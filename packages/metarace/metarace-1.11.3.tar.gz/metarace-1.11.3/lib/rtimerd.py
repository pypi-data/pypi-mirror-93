
# Metarace : Cycle Race Abstractions
# Copyright (C) 2012  Nathan Fraser
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

"""Remote timer daemon application."""

import pygtk
pygtk.require("2.0")

import gtk
import glib
#import gobject

import os
import sys
import logging
#import random

import metarace
import subprocess

from metarace import jsonconfig
from metarace import tod
from metarace import telegraph
from metarace import unt4
from metarace import strops
from metarace import timy
from metarace import thbc

CONFIGFILE = u'rtimerd.json'
LOGFILE = u'rtimerd.log'
LOGHANDLER_LEVEL = logging.DEBUG
APP_ID = u'rtimerd_1.0'  # configuration versioning
TIMERHANDLERS = {u'thbc': thbc.thbc,
                 u'timy': timy.timy,
                }
DEFAULT_TIMERHANDLER = u'timy'	# default is timy.

def timer_device(devstr=u''):
    """Return a pair: (device, port) for the provided device string."""
    (a, b, c) = devstr.partition(u':')
    devtype = DEFAULT_TIMERHANDLER
    if b:
        a = a.lower()
        if a in TIMERHANDLERS:
            devtype = a
        a = c   # shift port into a
    devport = a
    return((devtype, devport))

class rtimerd:
    """Timer application class."""
    def __init__(self, configpath=None):
        self.workers = {}
        self.workerports = {}
        # logger and log handler
        self.log = logging.getLogger()
        self.log.setLevel(logging.DEBUG)
        self.loghandler = None  # set in loadconfig to meet dir

        # meet configuration path and options
        if configpath is None:
            configpath = u'.'   # None assumes 'current dir'
        self.configpath = configpath

        # hardware connections
        self.remote = telegraph.telegraph()
        self.remoteuser = u''           # match against remote nick
        self.remoteport = u''           # only connect if requested
        self.remotechan = u'#timing'
        self.remote.set_pub_cb(self.remote_cb)
        self.shellenable = False
        self.shellkey = u''

        # remote procedure call
        self.cmdset = {
            u'hello':self.hello,
            u'rtimer_shell':self.shellproc,
            u'rtimer_exit':self.exitrtimer,
            u'rtimer_save':self.savertimer,
            u'rtimer_add':self.addrtimer,
            u'rtimer_del':self.delrtimer,
            u'rtimer_sync':self.syncrtimer,
            u'rtimer_start':self.startrtimer,
            u'rtimer_stop':self.stoprtimer,
            u'rtimer_status':self.statrtimer
        }

        self.started = False
        self.failcount = 0	# watch remote for failure
        self.failthresh = 2

    def savertimer(self, user=None, channel=None, text=None):
        """RPC savecofig."""
        ret = u'nack'
        if self.saveconfig():
            ret = u'ack'
        self.remote.send_cmd(chan=channel,
                                 hdr=ret,
                                 txt=u'Save')
        
    def exitrtimer(self, user=None, channel=None, text=None):
        """RPC Exit program."""
        self.remote.send_cmd(chan=channel,
                                 hdr=u'ack',
                                 txt=u'Exit')
        glib.idle_add(self.destroy)
        

    def statrtimer(self, user=None, channel=None, text=None):
        """RPC Request Status."""
        # timy will refuse this command, but THBC requires it
        if text in self.workers:
            self.workers[text].status()
            self.remote.send_cmd(chan=channel,
                                 hdr=u'ack',
                                 txt=u'Status: ' + repr(text))

    def syncrtimer(self, user=None, channel=None, text=None):
        """RPC Synchronise Worker Roughly."""
        # timy will refuse this command, but THBC requires it
        if text in self.workers:
            self.workers[text].sync()
            self.remote.send_cmd(chan=channel,
                                 hdr=u'ack',
                                 txt=u'Sync: ' + repr(text))

    def startrtimer(self, user=None, channel=None, text=None):
        """Request new session."""
        if text in self.workers:
            self.workers[text].start_session()
            self.remote.send_cmd(chan=channel,
                                 hdr=u'ack',
                                 txt=u'Start session: ' + repr(text))

    def stoprtimer(self, user=None, channel=None, text=None):
        """Request end session."""
        if text in self.workers:
            self.workers[text].stop_session()
            self.remote.send_cmd(chan=channel,
                                 hdr=u'ack',
                                 txt=u'Stop session: ' + repr(text))

    def addrtimer(self, user=None, channel=None, text=None):
        """RPC add worker."""
        args = text.split(unichr(unt4.US))
        if len(args) == 2:
            if self.add_worker(args[0], args[1]):
                self.remote.send_cmd(chan=channel,
                                 hdr=u'ack',
                                 txt=u'Add worker: ' + repr(args[0]))
            else:
                self.remote.send_cmd(chan=channel,
                                 hdr=u'nack',
                                 txt=u'Add worker: ' + repr(args[0]))
        
    def delrtimer(self, user=None, channel=None, text=None):
        """RPC delete worker."""
        if self.del_worker(text):	# only one arg
            self.remote.send_cmd(chan=channel,
                                 hdr=u'ack',
                                 txt=u'Delete worker: ' + repr(text))
        else:
            self.remote.send_cmd(chan=channel,
                                 hdr=u'nack',
                                 txt=u'Delete worker: ' + repr(text))

    def shellcmd(self, args):
        """Run args in subprocess and return the program output."""
        ret = u''
        try:
            ret = subprocess.check_output(args,stderr=subprocess.STDOUT)
        except Exception as e:
            ret = repr(e)
        return ret

    def shellproc(self, user=None, channel=None, text=None):
        """Dangerously execute shell command on remote sys as rtimer."""
        ret = u'nack'
        reply = None
        if self.shellenable:
            args = text.split(unichr(unt4.US))
            if len(args) > 1:
                shellkey = args[0]
                if shellkey == self.shellkey:	# lame
                    reply=self.shellcmd(args[1:])
                    ret = u'ack'
                else:
                    self.log.debug(u'Key mismatch: ' + repr(args[0]))
            else:
                self.log.debug(u'Short shell command: ' + repr(text))
        else:
            self.log.debug(u'Ignored attempt to run shell proc.')
        self.remote.send_cmd(chan=channel,
                                 hdr=ret,
                                 txt=reply)

    def hello(self, user=None, channel=None, text=None):
        """Identify to caller."""
        self.remote.send_cmd(chan=channel,
                             hdr=u'ident',
                             txt=u'rtimerd-' + metarace.VERSION
                                 + u' on ' + self.remote.srvid
                                 + u' ' + unicode(len(self.workers))
                                 + u' workers.')
        for wid in self.workers:
            self.remote.send_cmd(chan=channel, hdr=u'ack',
                   txt=unichr(unt4.US).join([wid,
                                             self.workerports[wid],
                                             self.workers[wid].unitno]))

    def remote_cb(self, cmd, nick, chan):
        """Handle unt message from remote (in main loop)."""
        if self.remoteuser and self.remoteuser.lower() != nick.lower():
            #self.log.debug(u'Ignoring command from ' + repr(nick))
            return False
        if cmd.header and cmd.header.lower() in self.cmdset:
            if u'#' not in chan:	# was a private message
                chan = nick
            self.cmdset[cmd.header](nick,chan,cmd.text)
        else:
            self.log.debug(u'Ignoring command: ' + repr(cmd.header))

    def saveconfig(self):
        """Save applications config."""
        cw = jsonconfig.config()
        cw.add_section(u'rtimerd')
        cw.set(u'rtimerd',u'id',APP_ID)
        cw.set(u'rtimerd',u'remoteport',self.remoteport)
        cw.set(u'rtimerd',u'remoteuser',self.remoteuser)
        cw.set(u'rtimerd',u'remotechan',self.remotechan)
        cw.set(u'rtimerd',u'shellenable',self.shellenable)
        cw.set(u'rtimerd',u'shellkey',self.shellkey)
        cw.set(u'rtimerd',u'workers',self.workerports)
        self.log.debug('Saving config to: ' + repr(CONFIGFILE))
        with open(CONFIGFILE,'wb') as f:
            cw.write(f)
        return True

    def loadconfig(self):
        """Load application config."""
        cr = jsonconfig.config({u'rtimerd':{
                                 u'remoteport':u'',
                                 u'remoteuser':u'',
                                 u'remotechan':u'#timing',
                                 u'id':u'',
                                 u'shellenable':False,
                                 u'shellkey':u'',
                                 u'workers':{}
                               }})
        cr.merge(metarace.sysconf, u'rtimerd')
        cwfilename = metarace.default_file(CONFIGFILE)

        # re-set log file
        if self.loghandler is not None:
            self.log.removeHandler(self.loghandler)
            self.loghandler.close()
            self.loghandler = None
        self.loghandler = logging.FileHandler(
                             os.path.join(self.configpath, LOGFILE))
        self.loghandler.setLevel(LOGHANDLER_LEVEL)
        self.loghandler.setFormatter(logging.Formatter(
                       '%(asctime)s %(levelname)s:%(name)s: %(message)s'))
        self.log.addHandler(self.loghandler)

        # check for config file, but not a big deal if missing
        try:
            with open(cwfilename, 'rb') as f:
                cr.read(f)
        except Exception as e:
            self.log.error(u'Reading app config: ' + repr(e))

        # set telegraph connection
        self.remoteuser = cr.get(u'rtimerd', u'remoteuser')
        self.remotechan = cr.get(u'rtimerd', u'remotechan')
        self.remoteport = cr.get(u'rtimerd', u'remoteport')
        self.remote.set_portstr(portstr=self.remoteport,
                             channel=self.remotechan)
        if self.remoteuser:
            self.log.info(u'Enabled remote control by: '
                          + repr(self.remoteuser))
        else:
            self.log.info(u'Promiscuous remote control enabled.')
        self.shellenable = strops.confopt_bool(cr.get(u'rtimerd',
                                                      u'shellenable'))
        self.shellkey = cr.get(u'rtimerd',u'shellkey')
        if self.shellenable:
            self.log.warning(u'Enabled remote shell command processing.')

        # Add any pre-configured workers
        workers = cr.get(u'rtimerd', u'workers')
        for wid in workers:
            self.add_worker(wid,workers[wid])

        # After load complete - check config and report. This ensures
        # an error message is left on top of status stack. This is not
        # always a hard fail and the user should be left to determine
        # an appropriate outcome.
        cid = cr.get(u'rtimerd', u'id')
        if cid and cid != APP_ID:
            self.log.error(u'Meet configuration mismatch: '
                           + repr(cid) + u' != ' + repr(APP_ID))

    def __timercb(self, evt):
        """Handle event from timer."""
        tvec = [evt.index, evt.source, evt.chan,
                evt.refid, evt.rawtime()]
        self.remote.send_cmd(u'timer',
                             unichr(unt4.US).join(tvec),
                             self.remotechan)
        
    def add_worker(self, wid, wport):
        """Add the worker with wid and wport and start a controlling thread."""
        ret = False
        if wid:
            if wid in self.workers:	# if exists, replace
                self.del_worker(wid)
            # then add
            try:
                (cdev,cport) = timer_device(wport)
                nt = TIMERHANDLERS[cdev](port=cport, name=wid)
                nt.setcb(self.__timercb)
                nt.start()
                nt.sane()
                if cdev == u'timy':
                    # arm all chans and lock
                    nt.armlock(True)
                    for c in range(0,9):
                        nt.arm(c)
                self.workers[wid] = nt
                self.workerports[wid] = wport
                ret = True
            except Exception as e:
                self.log.error(u'Adding worker: ' + repr(e))
        return ret

    def __jointhread(self, th, wid):
        """Try to join a terminated thread handle."""
        th.join(timeout=0.05)
        if th.isAlive():
            self.log.debug(u'Worker still running: ' + repr(wid))
            return True	# re-try later
        else:
            self.log.info(u'Worker terminated: ' + repr(wid))
            return False

    def del_worker(self, wid):
        """Delete the worker with wid."""
        ret = False
        if wid in self.workers:
            self.workers[wid].exit()
            glib.timeout_add_seconds(1, self.__jointhread,
                                        self.workers[wid], wid)
            del(self.workers[wid])
            del(self.workerports[wid])
            self.log.debug(u'Deleted worker with id: ' + repr(wid))
            ret = True
        else:
            self.log.warning(u'Worker not found: ' + repr(wid))
        return ret

    def start(self):
        """Start the application."""
        if not self.started:
            self.log.debug(u'App startup.')
            self.remote.start()
            self.started = True
            glib.timeout_add_seconds(10, self.__watchdog)

    def __watchdog(self, data=None):
        #for t in self.workers:
            #self.workers[t].status()
        if not self.remote.connected():
            self.failcount += 1
            self.log.debug(u'Remote not connected, count at: '
                            + repr(self.failcount))
            if self.failcount > self.failthresh:
                self.log.debug(u'Calling for reconnect.')
                self.remote.set_portstr(portstr=self.remoteport,
                                        channel=self.remotechan,
                                        force=True)
                self.failcount = 0
        else:
            self.failcount = 0
        # scan workers for dead workers
        return True	# _try_ to keep it going

    def shutdown(self, msg=u''):
        """Shut down application."""
        self.started = False
        wlist = [w for w in self.workers]
        for worker in wlist:
            self.del_worker(worker)
        self.remote.exit(msg)
        print (u'Waiting for remote to exit...')
        self.remote.join()

    def destroy(self):
        self.log.info(u'Controlled termination.')
        self.shutdown()
        gtk.main_quit()
        return False

def main(etype=None):
    """Run the timerd application."""
    configpath = None

    # expand configpath on cmd line to realpath _before_ doing chdir
    if len(sys.argv) > 2:
        print(u'usage: rtimerd [configdir]\n')
        sys.exit(1)
    elif len(sys.argv) == 2:
        rdir = sys.argv[1]
        if not os.path.isdir(rdir):
            rdir = os.path.dirname(rdir)
        configpath = os.path.realpath(rdir)

    metarace.init()
    if configpath is not None:
        os.chdir(configpath)
    app = rtimerd(configpath)
    app.loadconfig()
    app.start()
    try:
        metarace.mainloop()
    except:
        app.shutdown(u'Exception from main loop.')
        raise

if __name__ == '__main__':
    main()

