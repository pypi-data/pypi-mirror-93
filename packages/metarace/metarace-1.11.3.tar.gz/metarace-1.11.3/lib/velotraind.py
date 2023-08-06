
# Metarace : Cycle Race Abstractions
# Copyright (C) 2012-2015  Nathan Fraser
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Velodrome Training Timing Daemon"""
HELP = {
	u'filter': u'[+addid] [-delid] ...  edit passing filter',
        u'header': u'                       request current passing header',
        u'replay': u'[start] [end]          replay passings start to end',
        u'vanilla': u'                      request unprocessed passings',
        u'status': u'                       request system status',
        u'quit': u'                         end session',
}

import SocketServer
import logging
import logging.handlers
import threading
import Queue
import socket
import time
import random
import errno
import os
import glib
#import ntplib

import metarace
from metarace import tod
from metarace import unt4
from metarace import timy	# for sectormap/channels
from metarace import strops
from metarace import meteo
from metarace import thbchub
from metarace import jsonconfig

LF = u'\n'
APPINFO = u'\tVelodrome Training Daemon ' + metarace.VERSION
APPINFO += u'\r\n\tCommands:\r\n'
PORT = 8422
PACING = 0.5
CMDMAXLEN = 60	# truncate search buffer residual past maxlen
LOGFILE = u'.velotraind.log'
CONFIGFILE = u'.velotraind.conf'
PASSLEVEL = 50	# set decoder detection to this level
DEFSEQ = [u'c1',u'c4',u'c6',u'c3',u'c5',u'c7',u'c8',u'c2']
STATTHRESH = tod.tod(u'173')	# expiry threshold for decoder level status
MOTOPROX = tod.tod(u'0.5')	# threshold for moto assist
LOGDRIFT = 0.10			# start logging drift over this (float secs)
ISOTHRESH = tod.tod(u'40.0')	# automatically isolate new passings this
                                # much newer than last processed passing
ISOMAXAGE = tod.tod(u'8.0')	# choke queue for only this long
GATEDELAY = tod.tod(u'0.075')	# start gate trigger correction

CONFIG = {
  u'gate': u'000001',			# refid of start gate transponder
  u'moto': u'000002',			# refid of motorbike transponder
  u'trig': u'254',			# refid of sync trigger
  u'passlevel': PASSLEVEL,		# default read level in decoders
  u'listen': u'0.0.0.0',		# IP address server listens on
  u'port': PORT,			# Port server listens on
  u'uaddr': thbchub.THBC_UDP_ADDR,	# UDP timing ip address
  u'uport': thbchub.THBC_UDP_PORT,	# UDP timing port
  u'bcast': u'255.255.255.255',		# broadcast address for timing LAN
  u'sync': None,			# IP of synchronisation master
  u'gatesector': None,			# channel of start of gate sector
  u'gatesrc': None,			# channel of start gate loop
  u'authstr': None,			# reset auth string
  u'authip': [],			# authorised ips
  u'c1': None,				# IP of finish line C1
  u'c2': None,				# IP of PA / C2
  u'c3': None,				# IP of PB / C3
  u'c4': None,				# IP of 200m start / C4
  u'c5': None,				# IP of 100m split / C5
  u'c6': None,				# IP of 50m split / C6
  u'c7': None,				# IP of Pursuit QTR / C7
  u'c8': None,				# IP of 150m split / C8
  u'map': None,				# sectormap in use
  u'minspeed': 28.0,			# minimum sector speed
  u'maxspeed': 95.0,			# maximum sector speed
  u'mingate': 9.0,			# minimum gate start sector speed
  u'maxgate': 22.5,			# maximum gate start sector speed
  u'dhi': None,                         # DHI address for scoreboard
  u'splits': {				# split channel defs (balanced track)
      u'c1': { u'lap':u'c1', u'half':None, u'qtr':None,
               u'200':u'c4', u'100':u'c5', u'50':u'c8' },
      u'c2': { u'lap':u'c2', u'half':u'c3', u'qtr':u'c7',
               u'200':None, u'100':None, u'50':None },
      u'c3': { u'lap':u'c3', u'half':u'c2', u'qtr':u'c4',
               u'200':None, u'100':None, u'50':None },
      u'c4': { u'lap':u'c4', u'half':u'c7', u'qtr':u'c2',
               u'200':u'c6', u'100':u'c8', u'50':u'c1' },
      u'c5': { u'lap':u'c5', u'half':None, u'qtr':None,
               u'200':u'c8', u'100':u'c4', u'50':u'c6' },
      u'c6': { u'lap':u'c6', u'half':None, u'qtr':None,
               u'200':u'c5', u'100':u'c1', u'50':u'c4' },
      u'c7': { u'lap':u'c7', u'half':u'c4', u'qtr':u'c3',
               u'200':None, u'100':None, u'50':None },
      u'c8': { u'lap':u'c8', u'half':None, u'qtr':None,
               u'200':u'c1', u'100':u'c6', u'50':u'c5'},
  }
}

DECODERSANE = {
  u'Time of Day': True,
  u'GPS Sync': False,
  u'Active Loop': False,
  u'Detect Max': True,
  u'Protocol': 0,
  u'CELL Sync': False,
  u'Sync Pulse': False,
  u'Serial Print': False,
  u'Timezone Hour': 0,
  u'Timezone Min': 0,
  u'STA Level': PASSLEVEL,
  u'BOX Level': PASSLEVEL,
}

PASSORDER = [u'index', u'date', u'time', u'env',
             u'refid', u'speed', u'split', u'sector',
             u'dist', u'moto', u'elap', u'lap',
             u'half', u'qtr', u'200', u'100', u'50']
RAWPASSORDER = [u'index', u'date', u'time', u'env',
                u'refid', u'sector', u'tod']

def loadconfig(l):
    """Read in server config."""
    l.debug(u'Reading server config.')
    ret = jsonconfig.config({u'velotraind':CONFIG})

    # First overwrite inbuilt with system defaults
    ret.merge(metarace.sysconf, u'velotraind')

    # Then consult specifics
    cfile = metarace.default_file(CONFIGFILE)
    if os.path.exists(cfile):
        l.debug(u'Reading config from: ' + repr(CONFIGFILE))
        try:
            with open(cfile, 'rb') as f:
                ret.read(f)
        except Exception as e:
            print(u'Error reading server config: ' + unicode(e))

    # Return only config section data
    return ret.dictcopy()[u'velotraind']

class tcphandler(SocketServer.BaseRequestHandler):
    curfilt = None
    inbuf = u''

    def sendall(self, buf):
        """Try to send all of message in as many packets as required."""
        msglen = len(buf)
        sent = 0
        while sent < msglen:
            try:
                out = self.request.send(buf[sent:])
                if out == 0:
                    raise socket.error(u'Client socket broken.')
                sent += out
            except socket.error as e:
                if e.errno == errno.EAGAIN:
                    #self.server.log.debug(u'Client send queue full.')
                    time.sleep(0.10)
                else:
                    raise

    def showhelp(self, msg):
        """Show protocol help message."""
        omsg = APPINFO
        for c in [u'filter', u'header', u'status',
                  u'replay', u'vanilla', u'quit']:
            omsg += u'\t' + c + u' ' + HELP[c] + u'\r\n'
        omsg += u'help\r\n'
        self.sendall(omsg.encode(u'ascii', u'replace'))

    def doreplay(self, msg):
        """Request replay of messages from session store."""
        idstart = None
        idend = None
        if len(msg['args']) > 0:	# might be a start id
            idstart = strops.confopt_int(msg[u'args'][0])
        if len(msg['args']) > 1:        # might be an end id
            idend = strops.confopt_int(msg[u'args'][1])

        count = self.server.replay(self.refno, idstart, idend)
        self.doack(u'replay',[unicode(count)])

    def doheader(self):
        """Emit a header record to client."""
        dv = []
        for k in PASSORDER:
            dv.append(k)
        self.doack(u'header', dv)

    def dovanilla(self):
        """Ask server for a copy of all the unprocessed passings."""
        count = self.server.vanillapass(self.refno)
        self.doack(u'vanilla', [unicode(count)])

    def doclear(self, msg):
        """Ask server to clear data structures."""
        arg = []
        if len(msg['args']) > 0 and msg[u'args'][0] == self.server.cf[u'authstr']:
            if self.server.clearhub():
                arg.append(u'ok')
            else:
                arg.append(u'error')
        else:
            arg.append(u'notauth')
        self.doack(u'clear', arg)
        
    def doreset(self, msg):
        """Ask server for a reset if possible."""
        arg = []
        if len(msg['args']) > 0 and msg[u'args'][0] == self.server.cf[u'authstr']:
            if self.server.resethub():
                arg.append(u'ok')
            else:
                arg.append(u'error')
        else:
            arg.append(u'notauth')
        self.doack(u'zero', arg)

    def commandproc(self, msg):
        """Protocol command handler."""
        if u'filter'.find(msg[u'command']) == 0:
            self.setfilter(msg)
        elif u'replay'.find(msg[u'command']) == 0:
            #self.server.log.debug(self.refno + u' Client replay request.')
            self.doreplay(msg)
        elif u'vanilla'.find(msg[u'command']) == 0:
            self.server.log.debug(self.refno + u' Client vanilla request.')
            self.dovanilla()
        elif u'header'.find(msg[u'command']) == 0:
            #self.server.log.debug(self.refno + u' Client header request.')
            self.doheader()
        elif u'status'.find(msg[u'command']) == 0:
            #self.server.log.debug(self.refno + u' Client status request.')
            self.server.reqstatus(self.refno)
        elif u'zero'.find(msg[u'command']) == 0:
            #self.server.log.debug(self.refno + u' Client reset request.')
            self.doreset(msg)
        elif u'clear'.find(msg[u'command']) == 0:
            #self.server.log.debug(self.refno + u' Client clear request.')
            self.doclear(msg)
        elif u'quit'.find(msg[u'command']) == 0:
            #self.server.log.debug(self.refno + u' Client ended session.')
            self.running = False
        else:	# assume help
            #self.server.log.debug(self.refno + u' Client help request.')
            self.showhelp(msg)

    def setfilter(self, msg):
        """Set or clear entries in the session filter."""
        if len(msg[u'args']) == 0:
            self.server.log.debug(self.refno + u' Clear filter.')
            self.curfilt = None
        else:
            adds = set()
            dels = set()
            for a in msg[u'args']:
                if len(a) > 1:	# soft target, add without '+'
                    if a[0] == u'-':
                        dels.add(a[1:])
                    elif a[0] == u'+':
                        adds.add(a[1:])
                    else:
                        adds.add(a)
            if self.curfilt is None:
                self.curfilt = set()	# create
            if len(adds) > 0:
                self.curfilt = self.curfilt.union(adds)
            if len(dels) > 0:
                self.curfilt = self.curfilt.difference(dels)
            if len(self.curfilt) == 0:
                self.curfilt = None	# remove if empty after proc
        self.doack(u'filter', self.curfilt)

    def doack(self, ret, args=None):
        """Write ack to the output queue to follow a multi-line response."""
        self.outq.put_nowait({u'type':u'ack',
                         u'ret':ret,
                         u'args':args})

    def ack(self, msg):
        """Emit an acknowledge to the client - for correct ordering"""
        omsg = msg[u'ret']
        if msg[u'args'] is not None and len(msg[u'args']) > 0:
            omsg += u' ' + u' '.join(msg[u'args'])
        omsg += u'\r\n'
        self.sendall(omsg.encode(u'ascii',u'replace'))

    def status(self, msg):
        """Emit status message to socket."""
        # this is both response and acknowledge
        ovec = [u'status']
        for k in [u'clockstat', u'date', u'time', u'env',
                  u'drift',
                  u'c1', u'c2', u'c3', u'c4', u'c5', u'c6', u'c7', u'c8']:
            ovec.append(msg[k])
        omsg = u' '.join(ovec) + u'\r\n'
        self.sendall(omsg.encode(u'ascii',u'replace'))

    def rawpass(self, msg):
        """Emit a raw passing."""
        # this is a single line in a multi-response
        datvec = [u'rawpass']
        for k in RAWPASSORDER:
            datvec.append(msg[k])
        omsg = u' '.join(datvec) + u'\r\n'
        self.sendall(omsg.encode(u'ascii',u'replace'))

    def filter(self, msg):
        """Emit compatible messages to socket."""
        # this is a single line in a multi-response
        if self.curfilt is None or msg[u'refid'] in self.curfilt:
            datvec = [u'passing']
            for k in PASSORDER:
                datvec.append(msg[k])
            omsg = u' '.join(datvec) + u'\r\n'
            self.sendall(omsg.encode(u'ascii',u'replace'))
        else:
            #self.server.log.debug(self.refno + u' Filtered: ' + repr(msg))
            pass

    def readsock(self):
        """Read and process incoming messages."""
        try:
            inb = self.request.recv(2048)
            self.inbuf += inb.decode(u'ascii', u'replace')
            while LF in self.inbuf:
                (cmd, sep, self.inbuf) = self.inbuf.partition(LF)
                cvec = cmd.split()
                if len(cvec) > 0:
                    qmsg = {u'type':u'command',
                            u'command':cvec[0].lower(),
                            u'args':cvec[1:]}
                    self.outq.put_nowait(qmsg)
                else:
                    pass
            # if there's no LF and the residual is > MAXLEN, discard it
            if len(self.inbuf) > CMDMAXLEN:
                self.inbuf = u''	# 
        except socket.error as e:
            if e.errno == errno.EAGAIN:
                pass
            else:
                raise

    def handle(self):
        """Handle a single timing connection."""
        self.refno = repr(id(self))
        self.outq = Queue.Queue()	# this is the handler Q
        self.request.setblocking(0)	# check compat w/sendall
        #self.request.settimeout(2.0)
        self.server.log.info(self.refno + u' Connect: ' 
                              + repr(self.client_address))
        self.server.addclient(self.refno, self.outq)
        self.running = True
        try:
            while self.running:
                # read command phase
                try:
                    m = self.outq.get(True, PACING)
                    self.outq.task_done()
                    # handle message
                    if m[u'type'] == u'passing':
                        self.filter(m)
                    if m[u'type'] == u'rawpass':
                        self.rawpass(m)
                    elif m[u'type'] == u'status':
                        self.status(m)
                    elif m[u'type'] == u'command':
                        self.commandproc(m)
                    elif m[u'type'] == u'ack':
                        self.ack(m)
                    else:
                        # unknown message type
                        pass
                except Queue.Empty:
                    pass
                # check socket for new data
                self.readsock()

        except Exception as e:
            self.server.log.error(self.refno + u' Exception: ' + repr(e))
        self.server.delclient(self.refno)
        self.server.log.info(self.refno + u' Disconnect: '
                              + repr(self.client_address))
        self.request.close()

SocketServer.TCPServer.allow_reuse_address = True
SocketServer.TCPServer.request_queue_size = 3
class tcpcsrv(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    log = None		# logging object filled in by caller
    clist = {}		# map of connected clients
    pstore = []		# store of passings in this session
    hub = None		# handle/queue to server hub for commands out?
    syncmaster = None	# IP address of the synchronisation master
    rlock = threading.Lock() # reset lock
    cf = None		# copy of configuration map
    resetting = True	# status flag set in reset procedure
    met = None		# handle to environment object
    rawpass = []	# list of raw passing messages (includes system msgs)
    dstat = {}		# data store for decoder status info	c1->(level,tod)
    drifts = {}		# data store for decoder drift
    motos = {}		# store for most recent moto passing
    gate = None		# last gate trigger
    passq = {}		# passing queue buffer
    secmap = {}		# sector map for configured decoders
    offset = None	# maintain rough system clock offset from sync master
    dhi = None		# address of DHI scoreboard

    def initsectors(self):
        """Initialise the sector maps and data structures."""
        self.log.debug(u'SERVER: Reset passing data structures.')
        self.offset = tod.agg(0)
        for d in [u'c1',u'c2',u'c3',u'c4',u'c5',u'c6',u'c7',u'c8']:
            self.dstat[d] = (u'n/a',None)
            self.drifts[d] = tod.tod(u'0')
            self.motos[d] = None
        self.gate = None
        self.passq = {}
        self.rawpass = []

        # update sector map
        secsrc = timy.make_sectormap(self.cf[u'map'])
        self.log.debug(u'SERVER: building map for source '
                         + repr(self.cf[u'map']))
        self.secmap = {}
        last = None
        first = None
        prev = None
        for d in DEFSEQ:
            if d in self.cf and self.cf[d] is not None:
                self.secmap[d] = {u'prev':None, u'next':None,
                                  u'slen':None, u'sid':None,
                                  u'maxtime':None, u'mintime': None,
                                  u'lap':None, u'half':None, u'qtr':None,
                                  u'200':None, u'100':None, u'50':None}
                # check for split defs 
                if d in self.cf[u'splits']:
                    spmap = self.cf[u'splits'][d]
                    for split in [u'lap', u'half', u'qtr', u'200',
                                  u'100', u'50']:
                      if split in spmap:	# for degenerate config
                        spid = spmap[split]
                        if spid in self.cf and self.cf[spid] is not None:
                            startid = timy.chan2id(spid)
                            endid = timy.chan2id(d)
                            splen = secsrc[(startid,endid)]
                            sm = {u'src':spid,
                                  u'min':tod.dr2t(splen, self.cf[u'maxspeed']),
                                  u'max':tod.dr2t(splen, self.cf[u'minspeed']),
                                  u'len':splen}
                            self.secmap[d][split] = sm
                
                if first is None:
                    first = d
                last = d
                if prev is not None:
                    # fill in all sector data
                    self.secmap[prev][u'next'] = d # prev->next = this
                    self.secmap[d][u'prev'] = prev # this->prev = prev
                    startid = timy.chan2id(prev)
                    endid = timy.chan2id(d)
                    seclen = secsrc[(startid,endid)]
                    self.secmap[d][u'slen'] = seclen
                    self.secmap[d][u'sid'] = endid
                    self.secmap[d][u'mintime'] = tod.dr2t(seclen,
                                                     self.cf[u'maxspeed'])
                    self.secmap[d][u'maxtime'] = tod.dr2t(seclen,
                                                     self.cf[u'minspeed'])
                prev = d
        if first is not None and last is not None:
            # fill in the final sector that closes the loop
            self.secmap[last][u'next'] = first
            self.secmap[first][u'prev'] = last
            startid = timy.chan2id(last)
            endid = timy.chan2id(first)
            seclen = secsrc[(startid,endid)]
            self.secmap[first][u'slen'] = seclen
            self.secmap[first][u'sid'] = endid
            self.secmap[first][u'mintime'] = tod.dr2t(seclen,
                                             self.cf[u'maxspeed'])
            self.secmap[first][u'maxtime'] = tod.dr2t(seclen,
                                             self.cf[u'minspeed'])

        # also add the start 'gate' as an entrance sector
        startid = timy.chan2id(self.cf[u'gatesrc'])
        endid = timy.chan2id(self.cf[u'gatesector'])
        seclen = secsrc[(startid,endid)]
        self.secmap[u'gate'] = {u'prev':None, u'next':self.cf[u'gatesector'],
                                  u'slen':seclen, u'sid':endid,
                              u'maxtime':tod.dr2t(seclen, self.cf[u'mingate']),
                              u'mintime':tod.dr2t(seclen, self.cf[u'maxgate'])
                               }
        self.log.debug(u'SERVER: ' + unicode(len(self.secmap))
                               + u' sectors: ' + repr(self.secmap))

    def prepareq(self, refid):
        if refid not in self.passq:
            nq = {}
            for d in [u'lt', u'lc', u'choke',
                      u'c1',u'c2',u'c3',u'c4',
                      u'c5',u'c6',u'c7',u'c8']:
                nq[d] = None
            nq[u'q'] = tod.todlist(u'PQ')
            self.passq[refid] = nq
        return self.passq[refid]
    
    def terminate(self):
        self.log.debug(u'SERVER Shutting down socket.')
        self.socket.shutdown(socket.SHUT_RDWR)
        self.log.debug(u'SERVER Terminate connected handlers.')
        for c in self.clist.keys():
            try:
                self.clist[c].put_nowait({u'type':u'command',
                                      u'command':u'quit',
                                      u'args':[]})
            except:
                pass	# item removed while traversing list
        self.log.debug(u'SERVER Terminate server.')
        self.shutdown()
  
    def delclient(self, r):
        # called from worker threads - dangerous on iterations!
        del(self.clist[r])

    def addclient(self, r, q):
        # called from worker threads - dangerous on iterations!
        self.clist[r] = q

    def getstatus(self, data=None):
        """Broadcast a status request."""
        nt = tod.tod(u'now')
        for d in [u'c1',u'c2',u'c3',u'c4',u'c5',u'c6',u'c7',u'c8']:
            (level,tt) = self.dstat[d]
            if tt is None or nt-tt > STATTHRESH:
                self.dstat[d] = (u'n/a',None)
        ## expire any stale decoder status from data structure
        self.hub.pingall()
        return True

    def clockstat(self):
        """Return a system clock status string."""
        ret = u'error'
        try:
            #r = ntplib.NTPClient().request(u'localhost')
            self.log.debug(u'SERVER: mode={0}, stratum={1}, offset={2}'.format(
                                   0, 3,
                                   self.offset.as_seconds(3)))
            if True:	## r.stratum != 0:
                if abs(float(self.offset.as_seconds(3))) > 0.5:
                    ret = u'offset'
                    self.log.info(u'SERVER: System time offset detected: '
                                    + self.offset.rawtime(3))
                else:
                    ret = u'sync'
            else:
                ret = u'nosync'
        except Exception as e:
            self.log.error(u'SERVER: Error checking server NTP status: '
                             + repr(e))
        
        return ret

    def vanillapass(self, r):
        """Return all vanilla passings to client."""
        ret = -1
        try:
            c = 0
            for p in self.rawpass:
                p[u'index'] = unicode(c)
                self.clist[r].put_nowait(p)
                c += 1
            ret = c
        except Exception as e:
            self.log.error(u'SERVER Vanilla error: '
                           + repr(r) + u':' +repr(e))
        return ret

    def reqstatus(self, client=None):
        """Request status from server."""
        ## build a status object and then return to nominated clients.
        nt = tod.tod(u'now')
        dm = self.offset.rawtime(3)
        st = {u'type': u'status',
              u'clockstat': self.clockstat(),
              u'date': self.today(),
              u'time': nt.rawtime(places=2,zeros=True,hoursep=u':'),
              u'drift': dm,
              u'env': self.met.envstr(),
              }
        for d in [u'c1',u'c2',u'c3',u'c4',u'c5',u'c6',u'c7',u'c8']:
            st[d] = self.dstat[d][0]
            if d in self.drifts:
                st[d] += u',' + self.drifts[d].rawtime(3)
        self.status(st, client) 

    def status(self, status, client=None):
        """Add a status object and send to all or just client."""
        slist = []
        if client is None:
            slist = [c for c in self.clist]
        elif client in self.clist:
            slist = [client]
        for c in slist:
            try:
                self.clist[c].put_nowait(status)
            except Exception as e:
                self.log.error(u'SERVER Status error: ' 
                               + repr(c) + u':' +repr(e))

    def today(self):
        """Return a datestring for today."""
        return time.strftime(u'%F')

    def statuscb(self, src, m, data=None):
        """Handle status message from decoder."""
        chan = m.source.lower()
        statv = m.refid.split(u':')
        if len(statv) > 0 and u'c' in chan and statv[0].isdigit():
            self.dstat[chan] = (statv[0],m)
        return None

    def emit_env(self):
        """Try to send an environment update."""
        if self.dhi is not None:
          try:
            es = self.met.envstr().split(',')
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.0)
            s.connect(self.dhi)
            s.sendall(unt4.unt4(header='DC',text=es[0]).pack().encode('ascii', 'ignore'))
            s.sendall(unt4.unt4(header='RH',text=es[1]).pack().encode('ascii', 'ignore'))
            s.sendall(unt4.unt4(header='BP',text=es[2]).pack().encode('ascii', 'ignore'))
            s.shutdown(socket.SHUT_RDWR)
            s.close()
          except Exception as e:
            self.log.debug(u'SERVER: error sending env to scoreboard: '
                              + repr(e))

    def systempass(self, src, t, chan):
        """Process a system passing message."""
        if t.refid == self.cf[u'trig']:
            tom = tod.agg(60*int(round(float(t.as_seconds(2))/60.0)))
            self.drifts[chan] = tom - t
            if abs(float(self.drifts[chan].timeval)) > LOGDRIFT:
                self.log.debug(u'SERVER: Unexpected drift: ' + chan + u'@ '
                             + self.drifts[chan].rawtime(3))
            # record channel tod for drift data
            # use C2 (finish) to emit env vars to scoreboard
            if chan == u'c2':
                self.emit_env()
            
        elif t.refid == self.cf[u'moto']:
            self.log.debug(u'SERVER: Moto: ' + chan + u'@' + t.rawtime(2))
            self.motos[chan] = t
            # record moto over loop
        elif t.refid == self.cf[u'gate']:
            if chan == self.cf[u'gatesrc']:
                self.cleanqueues()
                self.log.debug(u'SERVER: Gate trigger: ' + t.rawtime(2))
                self.gate = t - GATEDELAY	# should be config
                po = {
                    u'type':u'passing',
                    u'date': self.today(),
                    u'time': self.gate.rawtime(places=2,
                                               zeros=True,hoursep=u':'),
                    u'env': self.met.envstr(),
                    u'refid': u'gate',
                    u'speed': u'n/a',
                    u'split': u'n/a',
                    u'sector': u'n/a',
                    u'dist': u'n/a',
                    u'moto': u'n/a',
                    u'elap': u'0.0',
                    u'lap': u'n/a',
                    u'half': u'n/a',
                    u'qtr': u'n/a',
                    u'200': u'n/a',
                    u'100': u'n/a',
                    u'50': u'n/a',
                }
                self.passing(po)
            else:
                self.log.debug(u'SERVER: Spurious gate: ' + chan
                                     + u'@' + t.rawtime(2))
        
    def passcb(self, src, t, data=None):
        """Hub calls this function for each passing event."""

        # note: this function is called in the hub thread, and queues
        #       data into client command queues. 
        if self.resetting:
            self.log.debug(u'SERVER: Ignored passing during reset: ' 
                             + repr(t))
            return None

        # patch invalid refid to reserved trigger
        if not t.refid:
            t.refid = u'1'
        cid = t.source.lower()

        # store the raw passing
        nt = tod.now()	# also used later
        self.rawpass.append({u'type':u'rawpass',
                             u'date':self.today(),
                             u'time':nt.rawtime(places=3,zeros=True,hoursep=u':'),
                             u'env':self.met.envstr(),
                             u'refid':t.refid,
                             u'sector': cid,
                             u'tod':t.rawtime(places=2,zeros=True,hoursep=u':')
                            })

        # update system offset if msg on channel 1
        if cid == u'c1':
            self.offset = nt - t
        elif cid not in self.dstat:
            self.log.info(u'SERVER: Spurious source ignored: ' + repr(cid))
            return None

        # allocate drift to non-trig passings
        if t.refid != self.cf[u'trig']:
            # danger: This circumvents all tod checks and assumes drift
            #         is small compared to tod ranges in use. This could
            #         break tod over midnight crossing - requires testing.
            #         The other assumption is that drift is slow enough
            #         to not be noticed during a particular run, and much
            #         slower than the top of minute triggers.
            t.timeval += self.drifts[cid].timeval

        # then process
        if t.refid in [self.cf[u'gate'], self.cf[u'moto'], self.cf[u'trig']]:
            # processpq? 
            self.systempass(src, t, cid)
            #if t.refid == self.cf[u'moto']:	# also process moto 
                #ps = self.prepareq(t.refid)
                #ps[u'q'].insert(t, cid) # insert this pass into queue
                #self.process_pq(t.refid, ps)
        else:
            ps = self.prepareq(t.refid)
            ps[u'q'].insert(t, cid) # insert this pass into queue
            self.process_pq(t.refid, ps)
        return None

    def cleanqueues(self):
        """Process all passing queues."""
        qlist = []
        for refid in self.passq:
            self.process_pq(refid, self.passq[refid])
            qlist.append(refid)
        self.log.debug(u'SERVER: Clean queues: ' + u', '.join(qlist))
        return False

    def isolated_match(self, cid, nt, hist):
        """Determine if this passing is isolated."""
        # special case: no history, or jut way too old - easy fix
        if hist[u'lc'] is None or (nt - hist[u'lt']) > ISOTHRESH:
            return True

        # otherwise be cautious
        if hist[u'choke'] is not None:
            age = tod.now() - nt
            if age > ISOMAXAGE:
                return True

        return False	# always choke at least once before isolating

    def sector_match(self, cid, nt, hist):
        """Determine if a new time is for a matching sector."""
        startid = self.secmap[cid][u'prev']
        comlen = None

        # special case check for gate override
        if cid == self.cf[u'gatesector'] and self.gate is not None:
            oktogo = False
            gs = self.secmap[u'gate']
            if hist[u'lc'] is not None and hist[u'lc'] == startid:
                # we have passing over gate loop, compare passings
                if self.gate > hist[u'lt']:
                    secelap = nt - self.gate
                    if secelap > gs[u'mintime'] and secelap < gs[u'maxtime']:
                        oktogo = True
                ## TODO: Test the false gate v hist comparison here, this can
                ##       happen when you have a rider on track and gate start,
                ##       requires two transponders.
            else:
                # no history OR out of order, just let gate override
                secelap = nt - self.gate
                if secelap > gs[u'mintime'] and secelap < gs[u'maxtime']:
                    oktogo = True

            if oktogo:	# overwrite is safe, modify history for the trig
                hist[u'lc'] = startid
                hist[u'lt'] = self.gate
                hist[startid] = self.gate
                return True	# and short-circuit

        # normal case: passing at speed over the sector
        if hist[u'lc'] is not None and hist[u'lc'] == startid:
            sd = self.secmap[cid]
            secelap = nt - hist[u'lt']
            if secelap > sd[u'mintime'] and secelap < sd[u'maxtime']:
                return True

        # all others are degenerate or isolated.
        return False

    def process_pq(self, refid, p):
        """Process the contents of the passing queue in p."""

        # assume we can visit all elems in Q:
        proclist = [j for j in p[u'q']]	# sorted!
        for j in proclist:
            cid = j.refid	# end of sector
            if self.sector_match(cid, j, p):
                #self.log.debug(u'SERVER: sector match: ' + cid)
                # fetch sector
                sm = self.secmap[cid]

                # compute sector time/speed info
                dist = u'{0:0.1f}'.format(sm[u'slen'])
                sid = unicode(sm[u'sid'])
                stime = p[u'lt']	# sector start time (checked)
                selap = j - stime	# sector elapsed time (checked)
                spdstr = selap.rawspeed(dist)

                # check for start gate and moto
                elap = u'n/a'
                if self.gate is not None and self.gate < j:
                    elap = unicode((j - self.gate).as_seconds(2))
                moto = u'norm'
                if cid in self.motos and self.motos[cid] is not None:
                    mt = self.motos[cid]
                    if mt < j and (j - mt) < MOTOPROX:
                        moto = u'moto'
                po = {
                    u'type':u'passing',
                    u'date': self.today(),
                    u'time': j.rawtime(places=2,zeros=True,hoursep=u':'),
                    u'env': self.met.envstr(),
                    u'refid': refid,	# no longer stored in tod
                    u'speed': spdstr,
                    u'split': unicode(selap.as_seconds(2)),
                    u'sector': sid,
                    u'dist': dist,
                    u'moto': moto,
                    u'elap': elap,
                    u'lap': u'n/a',
                    u'half': u'n/a',
                    u'qtr': u'n/a',
                    u'200': u'n/a',
                    u'100': u'n/a',
                    u'50': u'n/a',
                }
                for split in [u'lap', u'half', u'qtr',
                              u'200', u'100', u'50']:
                    # overwrite split if possible
                    if split in sm and sm[split] is not None:
                        spsrc = sm[split]
                        sc = spsrc[u'src']
                        if sc in p and p[sc] is not None:
                            selp = j - p[sc]
                            if selp > spsrc[u'min'] and selp < spsrc[u'max']:
                                po[split] = unicode(selp.as_seconds(2))

                # remove from queue
                p[u'q'].remove_first(cid)

                # save to history - this is now a processed sector
                p[u'lt'] = j
                p[u'lc'] = cid
                p[cid] = j
                p[u'choke'] = None

                # issue to all clients and continue
                self.passing(po)
            else:
                # the head of the queue doesn't match required data
                if self.isolated_match(cid, j, p):
                    #self.log.debug(u'SERVER: isolated match: ' + cid)
                    sm = self.secmap[cid]
                    sid = unicode(sm[u'sid'])
                    # check for start gate and moto
                    elap = u'n/a'
                    if self.gate is not None and self.gate < j:
                        elap = unicode((j - self.gate).as_seconds(2))
                    moto = u'norm'
                    if cid in self.motos and self.motos[cid] is not None:
                        mt = self.motos[cid]
                        if mt < j and (j - mt) < MOTOPROX:
                            moto = u'moto'
                    po = {
                        u'type':u'passing',
                        u'date': self.today(),
                        u'time': j.rawtime(places=2,zeros=True,hoursep=u':'),
                        u'env': self.met.envstr(),
                        u'refid': refid,	# no longer stored in tod
                        u'speed': u'n/a',
                        u'split': u'n/a',
                        u'sector': sid,
                        u'dist': u'n/a',
                        u'moto': moto,
                        u'elap': elap,
                        u'lap': u'n/a',
                        u'half': u'n/a',
                        u'qtr': u'n/a',
                        u'200': u'n/a',
                        u'100': u'n/a',
                        u'50': u'n/a',
                    }
                    for split in [u'lap', u'half', u'qtr',
                                  u'200', u'100', u'50']:
                        # overwrite split if possible
                        if split in sm and sm[split] is not None:
                            spsrc = sm[split]
                            sc = spsrc[u'src']
                            if sc in p and p[sc] is not None:
                                selp = j - p[sc]
                                if selp > spsrc[u'min'] and selp < spsrc[u'max']:
                                    po[split] = unicode(selp.as_seconds(2))
                    # remove from queue
                    p[u'q'].remove_first(cid)

                    # save to history - this is now a processed passing
                    p[u'lt'] = j
                    p[u'lc'] = cid
                    p[cid] = j
                    # don't unchoke yet - there may be multiple stale passes
                    # issue to all clients and continue
                    self.passing(po)
                else:
                    #self.log.debug(u'SERVER: Queue choked on: ' + cid
                                        #+ u'@' + unicode(j.as_seconds(2)))
                    p[u'choke'] = cid
                    break

    def passing(self, passob):
        """Add a passing object to server."""
        index = len(self.pstore)
        passob[u'index'] = unicode(index)
        self.pstore.append(passob)
        for c in self.clist.keys():
            try:
                self.clist[c].put_nowait(passob)
            except Exception as e:
                self.log.error(u'SERVER Passing error: '
                               + repr(c) + u':' +repr(e))

    def idlereset(self):
        self.resethub()
        return False

    def clearhub(self):
        """Like reset but don't talk to decoders."""
        ret = False
        if not self.rlock.acquire(False):
            self.log.debug(u'SERVER Clear/Reset already in progress.')
            return False
        try:
            self.log.debug(u'SERVER Clear...')
            self.resetting = True
            # clear pass index & reset data structures
            self.pstore = []
            self.initsectors()
            self.resetting = False
            ret = True
        except Exception as e:
            self.log.error(u'SERVER Clear error: ' + repr(e))
        finally:
            self.rlock.release()
        return ret

    def resethub(self):
        """Request reset for client."""
        ret = False
        if not self.rlock.acquire(False):
            self.log.debug(u'SERVER Reset already in progress.')
            return False
        try:
            self.log.debug(u'SERVER Reset...')
            self.resetting = True
            # stop & reset _all_ decoders
            for d in self.hub.hub:
                self.hub.stopsession(d)
                self.hub.wait()
                time.sleep(0.1)
                self.hub.sendto(thbchub.QUECMD, d)	# fetch config
                self.hub.wait()
                time.sleep(0.1)
                self.hub.configset(DECODERSANE, d)	# re-write config
                self.hub.wait()
                time.sleep(0.1)
            # clear pass index & reset data structures
            self.pstore = []
            self.initsectors()

            # wait for a clear block of time
            resid = int(tod.tod('now').as_seconds())%60
            while resid > 40:
                self.log.debug(u'SERVER Reset waiting [' + repr(resid) + u']') 
                time.sleep(float(62 - resid))
                resid = int(tod.tod('now').as_seconds())%60
            # set the trig time
            nt = tod.tod(60+ 60*(int(tod.tod(u'now').as_seconds())//60))
            (hr, mn, sc) = nt.rawtime(0, zeros=True,
                                  hoursep=u':', minsep=u':').split(u':')

            # prepare slaves for sync pulse
            confchg = {"Sync Pulse": False,
                         "CELL Sync Hour":int(hr),
                         "CELL Sync Min":int(mn),
                         "CELL Sync":True}
            for d in self.hub.hub:
                if d != self.syncmaster:
                    self.hub.configset(confchg, d)

            # prepare sync master
            self.hub.startsession(self.syncmaster)
            self.hub.wait()
            self.hub.sync()
            self.hub.wait()
            self.hub.configset({"Sync Pulse": True,
                                "Active Loop": True}, self.syncmaster)
            self.hub.wait()
            ret = True
            self.resetting = False
        except Exception as e:
            self.log.error(u'SERVER Reset error: ' + repr(e))
        finally:
            self.rlock.release()
        return ret

    def replay(self, r, idstart=None, idend=None):
        """Replay selected passings to client r."""
        count = 0
        if r in self.clist and len(self.pstore) > 0:
            count = 0
            # check start 
            ids = idstart
            if idstart is None:
                ids = 0					# clamp start
                idend = -1				# clamp end
            elif idstart < 0:
                ids = idstart % len(self.pstore)	# wrap down
            elif idstart >= len(self.pstore):
                ids = len(self.pstore) - 1		# or clamp end

            # copy corrected start to finish if no finish supplied
            if idend == None:
                idend = ids

            # check endpoint
            ide = idend
            if idend is None or idend >= len(self.pstore):
                ide = len(self.pstore) - 1		# clamp end
            elif ide < 0:
                ide = ide % len(self.pstore)	# wrap down

            # check range, with start as override	
            if ide < ids:
                ide = ids

            # issue each passing from store matching range to client r
            try:
                for i in range(ids, ide+1):
                    self.clist[r].put_nowait(self.pstore[i])
                    count += 1
            except Exception as e:
                self.log.error(u'SERVER Replay error: '
                               + repr(r) + u':' +repr(e))
                # notify client?
        return count

def main():
    metarace.init()

    # setup basic log
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    lh = logging.handlers.RotatingFileHandler(LOGFILE,
                  maxBytes=8388608, backupCount=2, encoding=u'utf8')
    lh.setLevel(logging.DEBUG)
    lh.setFormatter(logging.Formatter(
                          "%(asctime)s %(levelname)s:%(name)s: %(message)s"))
    log.addHandler(lh)
    
    # pull in config - except here should dump
    cf = loadconfig(log)
    log.debug(u'Got the config: ' + repr(cf))
    DECODERSANE[u'STA Level'] = cf[u'passlevel']
    DECODERSANE[u'BOX Level'] = cf[u'passlevel']
    
    # start env monitor
    y = meteo.meteo()
    
    # connect and start TCP srv
    tcpsrv = tcpcsrv((cf[u'listen'], cf[u'port']), tcphandler)
    tcpsrv_thread = threading.Thread(target=tcpsrv.serve_forever)
    tcpsrv_thread.daemon = True
    tcpsrv.log = log
    tcpsrv.cf = cf		# copy config into server object
    tcpsrv.met = y		# copy env probe into server object

    # prepare timing hardware connection
    hub = thbchub.thbchub()
    hub.broadcast = cf[u'bcast']
    hub.ipaddr = cf[u'uaddr']
    hub.portno = cf[u'uport']
    hub.setcb(tcpsrv.passcb, tcpsrv.statuscb)
    tcpsrv.hub = hub
    tcpsrv.syncmaster = cf[u'sync']
    glib.timeout_add_seconds(57,tcpsrv.getstatus)

    # add scoreboard dhi address if configured
    if cf['dhi'] is not None and len(cf['dhi']) > 1:
        tcpsrv.dhi = (cf['dhi'][0],cf['dhi'][1])

    # add all configured decoders
    for d in [u'c1',u'c2',u'c3',u'c4',u'c5',u'c6',u'c7',u'c8']:
        if cf[d] is not None:
            hub.add(cf[d], d)
            hub.stopsession(cf[d])
    hub.sync()
    glib.timeout_add_seconds(2, tcpsrv.idlereset)
    try:
        y.start()
        hub.start()
        tcpsrv_thread.start()
        metarace.mainloop()
    except:
        tcpsrv.terminate()
        hub.exit()
        y.exit()

    hub.join()
    y.join()

if __name__ == "__main__":
    main()
