
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

"""HL975 Display Console"""

import pygtk
pygtk.require("2.0")

import gtk
import glib
import pango
import gobject

import os
import sys
import logging
import serial
import random

import metarace

from metarace import jsonconfig
from metarace import tod
from metarace import telegraph
from metarace import unt4
from metarace import strops
from metarace import loghandler
from metarace import uiutil
from metarace import mrlogobmp

LOGHANDLER_LEVEL = logging.DEBUG
CONFIGFILE = u'hl975.json'
LOGFILE = u'hl975.log'
APP_ID = u'hl975_1.0'  # configuration versioning
ENCODING = 'iso8859-15'
HL975_BAUD = 9600
DISPLAYW = 192
DISPLAYH = 16
SCROLLMAX = 190	# chop a little less than 200 char scroll max
SCROLLCUT = 160	# try to find a word boundary up to 150 chars
EOT=0x04
STX=0x02
ETX=0x03
LF=0x0a
GFXHEAD = bytearray([EOT, EOT, 0x30, 0x47])
BRIGHTVALS = [0x31, 0x32, 0x33]
ELAPOFT = tod.tod('0.1')

DCONF_HDR = bytearray([0x82, 0x81, 0x20, 0x30,  # 2x1 displays, horizontal
                       0x85, 0x94, 0xb2,        # PWM levels 1, 2, 3 -0x80
                       0x20,    # spare...
                       0x20, 0x20, 0x20, 0x20,
                       0x20, 0x20, 0x20, 0x20])
DPANEL_HDR1 = bytearray([0x31,                  # 0x31=small/0x32=big
                        0x81, 0x82, 0x85, 0x86, # line addresses
                        0x80, 0x30, 0x31,       # disable CP mode
                        0x20, 0x20, 0x20, 0x20, # spare...
                        0x20, 0x20, 0x20, 0x20])
DPANEL_HDR2 = bytearray([0x31,
                        0x83, 0x84, 0x87, 0x88, # line addresses
                        0x80, 0x30, 0x31,       # disable CP mode
                        0x20, 0x20, 0x20, 0x20, # spare...
                        0x20, 0x20, 0x20, 0x20])
MRPANEL_SINGLE = [ [0x81, 0x82, 0x85, 0x86],
                   [0x83, 0x84, 0x87, 0x88] ]
MRPANEL_DBL = [ [0x81, 0x7f, 0x7f, 0x7f],
                [0x85, 0x7f, 0x7f, 0x7f] ]

## Panel layouts:

# 'single': 32 chars, 2 lines
#
#   ----------------------------------------
# 	0x81	0x82	|	0x83	0x84
#	0x85	0x86	|	0x87	0x88
#   ----------------------------------------
#
# 'double': 16 chars, 1 line double sized
#
#   ----------------------------------------
#       0x81		|	0x83
#
#   ----------------------------------------

def mk_config_buf(single=True):
    ret = bytearray()
    # add header and raw display blocks
    ret.extend(DCONF_HDR)
    ret.extend(DPANEL_HDR1)
    ret.extend(DPANEL_HDR2)
    # fill in panel layout
    layout = MRPANEL_SINGLE
    if not single:
        layout = MRPANEL_DBL
    for i in range(0,4):
       ret[16+1+i] = layout[0][i]
       ret[32+1+i] = layout[1][i]
    return ret

def iblrc(byteStr):
    ret = 0x00
    for b in byteStr:
        ret ^= b
    return ret

def str2hex( byteStr ):
    return ''.join( [ "%02X " % ord(x) for x in byteStr ] ).strip()

def byte2hex( byteStr ):
    return ''.join( [ "%02X " % x for x in byteStr ] ).strip()

def csum8(src):
    ret = 0
    for b in src:
        ret = (ret+b)&0xff
    return ret

def csum16(src):
    ret = 0
    for b in src:
        ret = (ret+b)&0xffff
    return ret

def i2b16(val):
    return bytearray([(val>>8)&0xff, val&0xff])

def i2b24(val):
    return bytearray([(val>>16)&0xff, (val>>8)&0xff, val&0xff])

def vc2dc(vcol, vrow):
    """Translate a vertical coordinate to display space."""
    ret = None
    if vcol >= 0 and vcol < 16:
        ret = (vrow+96, 15-vcol)	# reflected on 2nd panel
    elif vcol < 32:
        ret = (vrow, 31-vcol)	# reflected on 1st panel
    return ret

def cset(buf,vcol,vrow,csrc):
    """Draw the given character at the specified vcol and vrow."""
    for i in range(0,6):
        for j in range(0,8):
            bset(buf, i+vcol, j+vrow, csrc[i]&(1<<j))            

def nset(buf,vcol,vrow,csrc):
    """Draw the given supersize number at vcol, vrow."""
    for i in range(0,16):
        for j in range(0,22):
            bset(buf, i+vcol, j+vrow, csrc[i]&(1<<j))            

def bset(buf,vcol,vrow,val):
    """Set/clear bit in vertical buf with no checks."""
    (dcol, drow) = vc2dc(vcol, vrow)
    i=24*drow+dcol//8
    j=7-(dcol%8)
    if val:	# set
        buf[i] |= (1<<j)
    else:	# clear
        buf[i] &= ~(1<<j)

def logo2pbm(src):
    """Write out pbm."""
    with open(u'test.pbm', 'wb') as f:
        f.write('P4\n')
        f.write('192 16\n')
        f.write(src)

class hl975:
    """HL975 control console application."""

    def quit_cb(self, menuitem, data=None):
        """Quit the application."""
        self.running = False
        #self.window.destroy()

    def uscb_activate_cb(self, menuitem, data=None):
        """Request a re-connect to the uSCBsrv IRC connection."""
        if self.uscbport:
            self.log.info(u'Requesting re-connect to announcer: ' + 
                           repr(self.uscbport) + repr(self.uscbchan))
        else:
            self.log.info(u'Announcer not configured.')
            # but still call into uscbsrv...
        self.scb.set_portstr(portstr=self.uscbport,
                             channel=self.uscbchan,
                             force=True)

    def set_brightness(self, val):
        """Update local brightness."""
        nv = 0x31
        try:
            nv = int(val)
            if nv > 0 and nv < 4:
                nv = 0x30 + nv	# specified as 1, 2, 3
        except:
            self.log.info('Ignored invalid brightness: ' + repr(val))
        if nv in BRIGHTVALS:
            self.brightness = nv
        else:
            self.brightness = 0x31
            
    ## Help menu callbacks
    def menu_help_docs_cb(self, menuitem, data=None):
        """Display program help."""
        #metarace.help_docs(self.window)
        pass

    def menu_help_about_cb(self, menuitem, data=None):
        """Display metarace about dialog."""
        #metarace.about_dlg(self.window)
        pass

    def timeout(self):
        """Update status."""
        # 1: Terminate?
        if not self.running:
            return False
        # 2: Process?
        try:
            ntime = tod.tod(u'now')
            ntod = ntime.truncate(0)
            if ntime >= self.nc.truncate(1):
                self.tod = ntod
                self.process_timeout()
                # and advance one second
                self.nc += tod.ONE
            else:
                self.log.debug(u'Timeout called early: ' + ntime.rawtime())
                # no need to advance, desired timeout not yet reached
        except Exception as e:
            self.log.error(u'Timeout: ' + repr(e))

        # 3: Re-Schedule
        tt = tod.tod(u'now')+tod.tod(u'0.01')
        count = 0
        while self.nc < tt:     # ensure interval is positive
            if tod.MAX - tt < tod.ONE:
                self.log.debug(u'Midnight rollover.')
                break
            self.log.debug(u'May have missed an interval, catching up.')
            self.nc += tod.ONE  # 0.01 allows for processing delay
            count += 1
            if count > 10:
                break
        ival = int(1000.0 * float((self.nc - tod.tod(u'now')).timeval))
        if ival < 0 or ival > 10000:
            ival = 1000	# assume host time change
        glib.timeout_add(ival, self.timeout)

        # 4: Return False
        return False    # must return False

    def process_timeout(self):
        """Perform required timeout activities."""
        ctr = 20-int(self.tod.as_seconds())%21
        self.set_top_line(strops.truncpad(unicode(ctr),2,align='r'))
        self.log.debug(u'set: ' + repr(ctr))
        self.mirror_lines()
        # Check run state variables iff remote on:
        #if self.remote_enable:
            #self.set_top_line(self.tod.rawtime(0).rjust(8)+u'Goobers!')
            #self.set_bot_line(self.tod.rawtime(0).rjust(8)+u'Goobers!')
            #self.log.debug(u'Goobers.')

        # write dirty bufs to display
        if self.trig is not None:
            self.trig.setRTS(0)
        for j in range(0,8):
            if self.obuf[j] != self.lbuf[j]:
                self.setline(j)
        if self.trig is not None:
            self.trig.setRTS(1)

        # check connection status
        if not self.remote.connected():
            self.failcount += 1
            if self.failcount > self.failthresh:
                self.remote.set_portstr(force=True)
                self.failcount = 0
            self.log.debug(u'Telegraph connection failed, count = '
                           + repr(self.failcount))
        else:
            self.failcount = 0


    ## Window methods
    def app_set_title(self, extra=u''):
        """Update window title from meet properties."""
        title = u'hl975 Console'
        if self.title:
            title += u': ' + self.title
        #self.window.set_title(title)

    def app_destroy_cb(self, window, msg=u''):
        """Handle destroy signal and exit application."""
        if self.dosave:
            self.saveconfig()
        self.log.removeHandler(self.sh)
        #self.window.hide()
        self.log.info(u'App destroyed. ' + msg)
        glib.idle_add(self.app_destroy_handler)

    def app_destroy_handler(self):
        if self.started:
            self.shutdown()	# threads are joined in shutdown
        # close event and remove main log handler
        if self.loghandler is not None:
            self.log.removeHandler(self.loghandler)
        self.running = False
        # flag quit in main loop
        gtk.main_quit()
        return False

    def shutdown(self, msg=''):
        """Cleanly shutdown threads and close application."""
        self.started = False

        #self.window.hide()	# usually already called
        self.remote.exit(msg)
        self.close_display()
        print (u'Waiting for remote to exit...')
        self.remote.join()

    def start(self):
        """Start the timer and rfu threads."""
        if not self.started:
            self.log.debug(u'App startup.')
            self.remote.start()
            self.started = True

    ## UI callbacks

    def load_vfonts(self):
        """Load the vertical emulation fonts."""
        try:
            # Start with rotated board charset
            filename=metarace.default_file(u'ThFont-ISO8859-15.bmp')
            pb = gtk.gdk.pixbuf_new_from_file(filename)
            w = pb.get_width()
            h = pb.get_height()
            if h == 8 and w == 1344:
                self.vfont = []
                px = pb.get_pixels()
                pxcount = 3	# RGB
                if pb.get_has_alpha():
                    pxcount = 4	# RGBA
                self.log.debug(u'Total pixels: ' + repr(len(px)/pxcount))

                # read in each char
                for i in range(0,224):
                    thischar = bytearray(6)
                    charof = pxcount*6*i
                    for j in range(0,8):
                        rowstart = j*pxcount*1344 + charof
                        for k in range(0,6):
                            srcpos = rowstart + pxcount*k
                            mval = 0
                            for p in range(0,3):
                                mval += ord(px[srcpos+p])
                            if mval < 384:
                                thischar[k] |= (1<<j)
                    self.vfont.append(thischar)
                self.log.debug(u'Loaded vertical emulation font.')
            else:
                self.log.warn(u'Invalid font dimension: ' + unicode(w) 
                                 + u'x' + unicode(h))
            # Then load the xtra large vertical font
            filename=metarace.default_file(u'ThFont-Numeric-16x22.bmp')
            pb = gtk.gdk.pixbuf_new_from_file(filename)
            w = pb.get_width()
            h = pb.get_height()
            if h == 22 and w == 192:
                self.vlfont = []
                px = pb.get_pixels()
                pxcount = 3	# RGB
                if pb.get_has_alpha():
                    pxcount = 4	# RGBA
                self.log.debug(u'Total pixels: ' + repr(len(px)/pxcount))

                # read in each char
                for i in range(0,12):	# 12 chars
                    thischar = []
                    for l in range(0,16): thischar.append(0x00000000)
                    charof = pxcount*16*i	# of width 16
                    for j in range(0,22):	# and height 22
                        rowstart = j*pxcount*192 + charof # rows of 192px
                        for k in range(0,16):	# width 16 px
                            srcpos = rowstart + pxcount*k
                            mval = 0
                            for p in range(0,3):
                                mval += ord(px[srcpos+p])
                            if mval < 384:
                                thischar[k] |= (1<<j)
                    self.vlfont.append(thischar)
                self.log.debug(u'Loaded large vertical numeric font.')
            else:
                self.log.warn(u'Invalid font dimension: ' + unicode(w) 
                                 + u'x' + unicode(h))
        except Exception as e:
            self.log.error(u'Loading emulation font: ' + repr(e))
            self.vfont = None

    def bmp2dimg(self, filename):
        """Try and load the supplied image as dimg array."""
        try:
            pb = gtk.gdk.pixbuf_new_from_file(filename)
            w = pb.get_width()
            h = pb.get_height()
            if w != DISPLAYW or h != DISPLAYH:
                self.log.info(u'Source dimension: '
                               + repr(w) + u'x' + repr(h)
                               + u', scaling image.')
                pb = pb.scale_simple(DISPLAYW, DISPLAYH, gtk.gdk.INTERP_HYPER)
            w = pb.get_width()
            h = pb.get_height()
            self.log.debug(u'Read image: ' + repr(w) + u'x' + repr(h))
            px = pb.get_pixels()
            pxcount = 3	# RGB
            if pb.get_has_alpha():
                pxcount = 4	# RGBA
            self.log.debug(u'Total pixels: ' + repr(len(px)/pxcount))
            data = bytearray()
            pcount = 0
            acc = 0x00			# pixel accumulator
            for i in range(0,16):	# each row
                rof = i * 192 * pxcount
                for j in range(0,192):	# each col
                    pof = rof + j * pxcount
                    mval = 0
                    for k in range(0,3):
                        mval += ord(px[pof+k])
                    acc <<= 1
                    if mval > 384:
                        acc |= 0x01
                    pcount += 1
                    if pcount%8 == 0:
                        data.append(acc)
                        acc = 0x00
            self.log.debug(u'Data packed mono: '
                            + repr(len(data)) + u' bytes')
            self.logo = data
        except Exception as e:
            self.log.error(u'Loading logo file: ' + repr(e))
            self.logo = mrlogobmp.METARACE

    def but_config_clicked_cb(self, button, data=None):
        """Start config."""
        self.log.debug(u'App config cb.')
        self.dosave = True
        # re-write config to display
        conf = mk_config_buf()
        self.log.debug(u'Send Config: ' + repr(conf))
        self.stdcmd(0x91, ord('S'), conf)
        self.log.debug(u'Clear')
        self.serialwrite(chr(STX) + chr(0x90) + '111234567890' + chr(LF))
        self.serialwrite(chr(STX) + chr(0xA0) + '112345678' + chr(LF))

    def but_man_clicked_cb(self, button, data=None):
        """Manual display set."""
        self.log.debug(u'Manual display override.')
        #self.set_top_line(self.line0.get_text().decode('utf-8'))
        #self.set_bot_line(self.line1.get_text().decode('utf-8'))

    def set_top_line(self, msg):
        msg = strops.truncpad(msg, 16, elipsis=False)
        self.obuf[0] = self.obuf[2] = msg[0:8]
        self.obuf[1] = self.obuf[3] = msg[8:16]

    def set_bot_line(self, msg):
        msg = strops.truncpad(msg, 16, elipsis=False)
        self.obuf[4] = self.obuf[6] = msg[0:8]
        self.obuf[5] = self.obuf[7] = msg[8:16]
    
    def but_logo_clicked_cb(self, button, data=None):
        """Draw logo on display."""
        self.set_remote_disable()
        self.log.debug(u'Draw logo.')
        self.gfxcmd(0x30, 'E', bytearray([0xf0]))
        self.gfxcmd(0x30, 'W', 
                bytearray([0xf0]) + i2b24(0x00) + self.logo[0:0x80])
        self.gfxcmd(0x30, 'W',
                bytearray([0xf0]) + i2b24(0x80) + self.logo[0x80:0x100])
        self.gfxcmd(0x30, 'W',
                bytearray([0xf0]) + i2b24(0x100) + self.logo[0x100:0x180])
        self.gfxcmd(0x30, 'V',
                bytearray([0xf0]) + i2b24(0x180) + i2b16(csum16(self.logo)))

    def do_scroll(self, scrollmsg):
        scrollmsg = scrollmsg.rstrip()
        self.scrolltxt = scrollmsg
        if len(scrollmsg) > SCROLLMAX:
            scrollmsg = strops.truncpad(scrollmsg, SCROLLMAX)
            # try to truncate on a word boundary
            idf = scrollmsg.rfind(u' ')
            if idf > SCROLLCUT:
                scrollmsg = scrollmsg[0:idf].rstrip() + u' ...'
        if len(scrollmsg) > 0:
            self.serialwrite(chr(STX) + chr(0x80) + '11' +
                          scrollmsg.encode(ENCODING, 'replace') + chr(LF))
            #self.log.debug(u'Wrote msg: ' + repr(scrollmsg))
        else:
            #self.log.debug('Nothing to scroll.')
            self.scrolloff_clicked_cb(None)

    def scrolltext_activate_cb(self, entry, data=None):
        """Copy scrolling text to display on bottom line."""
        scrollmsg = self.scrolltext.get_text().decode('utf-8').rstrip()
        if len(scrollmsg) > SCROLLMAX:
            scrollmsg = strops.truncpad(scrollmsg, SCROLLMAX)
            # try to truncate on a word boundary
            idf = scrollmsg.rfind(u' ')
            if idf > SCROLLCUT:
                scrollmsg = scrollmsg[0:idf].rstrip() + u' ...'
        if len(scrollmsg) > 0:
            self.serialwrite(chr(STX) + chr(0x80) + '11' +
                          scrollmsg.encode(ENCODING, 'replace') + chr(LF))
            #self.log.debug(u'Wrote msg: ' + repr(scrollmsg))
        else:
            #self.log.debug('Nothing to scroll.')
            self.scrolloff_clicked_cb(None)

    def scrolloff_clicked_cb(self, button, data=None):
        """Terminate a scrolling message."""
        #self.log.info(u'Scroll text terminated.')
        for j in [0,1,2,3]:
            self.lbuf[j] = u''	# re-display top line from obuf
        self.serialwrite(chr(STX) + chr(0x90) + '111234567890' + chr(LF))

    def set_remote_enable(self):
        #self.line0.set_sensitive(False)
        #self.line1.set_sensitive(False)
        #uiutil.buttonchg(self.but_remote, uiutil.bg_armstart,'Remote')
        self.clearlines()	# refresh cache
        self.remote_enable = True

    def set_remote_disable(self):
        #self.line0.set_sensitive(True)
        #self.line1.set_sensitive(True)
        #uiutil.buttonchg(self.but_remote, uiutil.bg_armfin,'Local')
        self.remote_enable = False

    def but_remote_clicked_cb(self, button, data=None):
        """Toggle remote control."""
        if self.remote_enable:
            self.set_remote_disable()
        else:
            self.set_remote_enable()

    def but_clear_clicked_cb(self, button, data=None):
        """Request clear on display."""
        self.reset()		# reset all but finpanel runtime vars
        self.clearlines()	# empty local output buffer
        self.clearall()

    ## App functions

    def reset(self):
        """Reset run state."""
        self.elapstart = None
        self.elapfin = None
        self.finstr = None
        self.timerstat = u'running'	# default assume run state
        self.distance = None
        self.laplbl = None
        self.laptype = None
        self.lapstart = None
        self.lapfin = None
        #self.ttrank = None	# tt data persists over ERP
        #self.ttno = None
        #self.ttname = None
        #self.ttcat = None
        #self.tttime = None

    def serialwrite(self, cmd):
        """Output command blocking."""
        try:
            if self.scb:
                self.scb.write(cmd)
        except Exception as e:
            self.log.error(u'Writing to scoreboard: ' + repr(e))

    def parse_reply(self, rbuf=''):
        """Try to interpret scoreboard response string."""
        if len(rbuf) > 7:	# long enough for hdr/foot/etx/lrc
            if rbuf[0] == chr(EOT) and rbuf[1] == chr(EOT):
                if rbuf[4] == 'D' and rbuf[5] == 'I':
                    di = ''
                    for c in rbuf[6:]:
                        if c == chr(ETX):
                            break
                        else:
                            di += c
                    self.log.info(u'Ident: ' + repr(di))
                else:
                    self.log.info(u'Response: ' + repr(rbuf))

    def serialread(self):
        """Read from serial blocking."""
        try:
            if self.scb:
                self.parse_reply(self.scb.read(1024))
        except Exception as e:
            self.log.error(u'Reading from scoreboard: ' + repr(e))

    def gfxcmd(self, addr, code, data):
        """Send a raw graphic command."""
        dimbuf = i2b16(len(data))
        cmd = GFXHEAD[0:]
        cmd.append(code)
        cmd.extend(dimbuf)
        cmd.extend(data)
        csum = csum8(cmd)
        cmd.append(csum)
        self.serialwrite(str(cmd))	# bytes to str -> problem in 3+
        self.serialread()

    def stdcmd(self, addr, code, data=bytearray()):
        """Send a IBLE Standard code command."""
        cmd = bytearray([EOT, EOT, addr, STX, code])
        if len(data) > 0:
            cmd.extend(data)
        cmd.append(ETX)
        cmd.append(iblrc(cmd[2:]))
        self.serialwrite(str(cmd))
        self.serialread()

    def remote_cb(self, cmd, nick, chan):
        """Handle unt message from remote (in main loop)."""
        if self.remoteuser and self.remoteuser.lower() != nick.lower():
            #self.log.debug(u'Ignoring command from ' + repr(nick))
            return False

        #self.log.debug(u'Command from ' + repr(nick) + u': '
                       #+ repr(cmd.header) + u'::' + repr(cmd.text))
        if cmd.header == u'start':
            self.elapstart = tod.str2tod(cmd.text)
        elif cmd.header == u'finish':
            self.elapfin = tod.str2tod(cmd.text)
        elif cmd.header == u'redraw' and cmd.text == u'timer':
            # fake a timeout in the cb
            self.process_timeout()
        elif cmd.header == u'lapstart':
            self.lapstart = tod.str2tod(cmd.text)
        elif cmd.header == u'lapfin':
            self.lapfin = tod.str2tod(cmd.text)
        elif cmd.header == u'finstr':
            if cmd.text:
                self.finstr = cmd.text
            else:
                self.finstr = None	# force None for empty string
        elif cmd.header == u'laplbl':
            if cmd.text:
                self.laplbl = cmd.text
            else:
                self.laplbl = None	# force None for empty string
        elif cmd.header == u'laptype':
            if cmd.text:
                self.laptype = cmd.text
            else:
                self.laptype = None	# force None for empty string
        elif cmd.header == u'distance':
            self.distance = None
            try:
                a = float(cmd.text)
                if a > 0.1:
                    self.distance = a
            except:
                self.log.debug(u'Invalid distance: ' + repr(cmd.text))
        elif cmd.header == u'finpanel':
            fpvec = cmd.text.split(unichr(unt4.US))
            self.ttrank = None
            self.ttno = None
            self.ttname = None
            self.ttcat = None
            self.tttime = None
            if len(fpvec) > 4:	# rank/no/name/cat/time
                if fpvec[0]:
                    self.ttrank = fpvec[0]
                if fpvec[1]:
                    self.ttno = fpvec[1]
                if fpvec[2]:
                    self.ttname = fpvec[2]
                if fpvec[3]:
                    self.ttcat = fpvec[3]
                if fpvec[4]:
                    self.tttime = fpvec[4]
        elif cmd.header == u'scrollmsg':
            self.do_scroll(cmd.text)
            #self.scrolltext.set_text(cmd.text)
            #self.scrolltext.activate()
        elif cmd.header == u'timerstat':
            self.timerstat = cmd.text
        elif cmd.header == u'brightness':
            self.set_brightness(cmd.text)
        elif cmd.header == u'image':
            if cmd.text:
                glib.idle_add(self.set_logo, cmd.text, True)
            else:
                self.logofile = None
                self.logo = mrlogobmp.METARACE
                self.but_clear_clicked_cb(None)
        elif cmd.header == u'clearall':
            self.but_clear_clicked_cb(None)
        elif cmd.header == u'leaderboard':
            lvec = cmd.text.split(unichr(unt4.US))
            glib.idle_add(self.draw_vpage, lvec)
        elif cmd.header == u'eliminated':
            glib.idle_add(self.draw_vnum, cmd.text)
        elif cmd.erp:	# general clearing
            self.reset()
        return False

    def draw_vnum(self, num):
        """Draw the supplied number to the top of the vpanel supersized."""
        # based on geometry: 32x96, chars of 16x22, 1 line of 2 chars
        if self.logo is None:
            self.logo = bytearray(384)	# 192x16/8
        num = num.translate(strops.INTEGER_UTRANS)
        nl = 10
        nh = 10
        if len(num) > 0 and num[0].isdigit():
            nl = int(num[0])
        if len(num) > 1 and num[1].isdigit():
            nh = int(num[1])

        if self.vlfont is not None:
            oft = 0 #offset down panel
            nset(self.logo, 0, 0, self.vlfont[nl])
            nset(self.logo, 16,0, self.vlfont[nh])
            oft += 22
            while oft < 96:
                # erase remainder
                for i in range(0,32):
                    bset(self.logo, i, oft, 0)
                oft += 1
            self.but_logo_clicked_cb(None)
        #logo2pbm(self.logo)
        return False

    def draw_vpage(self, page):
        """Draw the supplied vertical page spec into dimg and display."""
        # based on geometry: 32x96, chars of 6x8, lines of 5 chars
        # NOT OPTIMISED IN ANY WAY!
        if self.logo is None:
            self.logo = bytearray(384)	# 192x16/8
        linesrc = [0,0,0,1, 1,1,1,1,
                   1,1,1,1, 1,1,1,1,
                   1,1,1,1, 1,1,1,1,
                   1,1,1,1, 1,0,0,0]
        if self.vfont is not None:
            oft = 0 #offset down panel
            for line in page:
                if oft > 88:
                    break	# terminate at end of board
                if line == u'-':
                    #ll draw lap separator
                    for i in range(0,32):
                        bset(self.logo, i, oft, linesrc[i])
                        bset(self.logo, i, oft+1, 0)
                    oft += 2
                else:
                    line = strops.truncpad(
                              line.translate(strops.PLACELIST_UTRANS),
                              5).encode('ascii','ignore')
                    cset(self.logo, 0, oft, self.vfont[ord(line[0])-0x20])
                    cset(self.logo, 6, oft, self.vfont[ord(line[1])-0x20])
                    for i in range(0,8):
                        bset(self.logo, 12,oft+i, 0)
                        bset(self.logo, 13,oft+i, 0)
                    cset(self.logo, 14, oft, self.vfont[ord(line[2])-0x20])
                    cset(self.logo, 20, oft, self.vfont[ord(line[3])-0x20])
                    cset(self.logo, 26, oft, self.vfont[ord(line[4])-0x20])
                    oft += 8
            while oft < 96:
                # erase remainder
                for i in range(0,32):
                    bset(self.logo, i, oft, 0)
                oft += 1
            self.but_logo_clicked_cb(None)
        #logo2pbm(self.logo)
        return False

    def set_logo(self, filename, show=False):
        self.logofile = None
        if filename:
            self.logofile = filename
            bmpfilename = metarace.default_file(self.logofile)
            self.bmp2dimg(bmpfilename)
            if show:
                self.but_logo_clicked_cb(None)
        else:
            self.logo = mrlogobmp.METARACE
        return False

    def mirror_lines(self):
        """Copy line buffers back to UI."""
        #self.line0.set_text(self.obuf[0]+self.obuf[1])
        #self.line1.set_text(self.obuf[4]+self.obuf[5])
        return False

    def setline(self, line):
        """Copy line to display."""
        cmd = (chr(STX) + chr(0x31 + line) + chr(self.brightness)
                + self.obuf[line].encode(ENCODING,'replace') + chr(LF))
        self.serialwrite(cmd)
        self.lbuf[line] = self.obuf[line]

    def clearlines(self):
        """Empty local caches."""
        for j in range(0,8):
            self.obuf[j] = u''.ljust(8)
            self.lbuf[j] = u'01234567'

    def clearall(self):
        """Call general clearing on display."""
        self.log.info(u'Clear display.')
        self.serialwrite(chr(STX) + chr(0x90) + '111234567890' + chr(LF))
        #self.serialwrite(chr(STX) + chr(0xA0) + '112345678' + chr(LF))

    def close_display(self):
        """Close serial port."""
        if self.scb is not None:
            self.log.info(u'Closing serial port.')
            self.scb.close()	# serial port close
            self.scb = None		# release handle

    def reconnect_display(self):
        """Re-connect to display serial port."""
        self.close_display()
        self.log.debug('Connecting serial port: ' + repr(self.port))
        try:
            self.scb = serial.Serial(self.port, HL975_BAUD, timeout=0.2)
            if self.trigport is not None:
                self.trig = serial.Serial(self.trigport, HL975_BAUD)
            self.stdcmd(0x40, ord('I'))
        except Exception as e:
            self.log.error(u'Opening serial port: ' + repr(e))
            self.scb = None

    def saveconfig(self):
        """Save current config to disk."""
        cw = jsonconfig.config()
        cw.add_section(u'hl975')
        cw.set(u'hl975', u'id', APP_ID)
        cw.set(u'hl975', u'port', self.port)
        cw.set(u'hl975', u'brightness', unichr(self.brightness))
        cw.set(u'hl975', u'remoteport', self.remoteport)
        cw.set(u'hl975', u'remotechan', self.remotechan)
        cw.set(u'hl975', u'remoteuser', self.remoteuser)
        cw.set(u'hl975', u'logo', self.logofile)
        cw.set(u'hl975', u'loglevel', self.loglevel)
        cw.set(u'hl975', u'maxlaptime', self.maxlaptime.rawtime())
        #cw.set(u'hl975', u'toplinetext',
                         #self.line0.get_text().decode('utf-8'))
        #cw.set(u'hl975', u'botlinetext',
                         #self.line1.get_text().decode('utf-8'))
        cw.set(u'hl975', u'scrolltext',
                         self.scrolltxt)
                         #self.scrolltext.get_text().decode('utf-8'))

        cwfilename = os.path.join(self.configpath, CONFIGFILE)
        self.log.debug(u'Saving app config to ' + repr(cwfilename))
        with open(cwfilename , 'wb') as f:
            cw.write(f)

    def loadconfig(self):
        """Load app config from disk."""
        cr = jsonconfig.config({u'hl975':{
               u'id':'',
               u'port':u'',
               u'trigport':None,
               u'remoteport':u'',
               u'remotechan':u'',
               u'remoteuser':u'',
               u'loglevel':unicode(logging.INFO),
               u'brightness':0x31,
               u'logo':u'',
               u'toplinetext':u'',
               u'botlinetext':u'',
               u'scrolltext':u'',
               u'maxlaptime':u'30:00'
              }})
        cr.add_section(u'hl975')
        cwfilename = metarace.default_file(CONFIGFILE)
        # read in sysdefaults before checking for config file
        cr.merge(metarace.sysconf, u'hl975')

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

        # check for config file
        try:
            with open(cwfilename, 'rb') as f:
                cr.read(f)
        except Exception as e:
            self.log.error(u'Reading app config: ' + repr(e))

        # set uSCBsrv connection
        self.remoteuser = cr.get(u'hl975', u'remoteuser')
        self.remotechan = cr.get(u'hl975', u'remotechan')
        self.remoteport = cr.get(u'hl975', u'remoteport')
        self.remote.set_portstr(portstr=self.remoteport,
                             channel=self.remotechan)
        if self.remoteuser:
            self.log.info(u'Enabled remote control by: '
                          + repr(self.remoteuser))
        else:
            self.log.info(u'Promiscuous remote control enabled.')

        # set display serial ports
        self.port = cr.get(u'hl975', u'port')
        self.trigport = cr.get(u'hl975', u'trigport')
        self.reconnect_display()

        # configurable log level on UI (does not change log file)
        self.loglevel = strops.confopt_posint(cr.get(u'hl975', u'loglevel'),
                                              logging.INFO)
        #self.sh.setLevel(self.loglevel)

        # brightness
        self.set_brightness(cr.get(u'hl975', u'brightness'))

        # load logo
        lgfile = cr.get(u'hl975', u'logo') 
        self.logofile = None
        if lgfile:
            self.logofile = lgfile
            bmpfilename = metarace.default_file(lgfile)
            self.bmp2dimg(bmpfilename)

        # load vertical emulation fonts
        self.load_vfonts()

        # check the maximum lap time field
        mlap = tod.str2tod(cr.get(u'hl975',u'maxlaptime'))
        if mlap is not None:
            self.maxlaptime = mlap

        # restore strings
        #self.line0.set_text(cr.get(u'hl975', u'toplinetext')[0:16])
        #self.line1.set_text(cr.get(u'hl975', u'botlinetext')[0:16])
        #self.scrolltext.set_text(cr.get(u'hl975', u'scrolltext'))
        self.scrolltxt = (cr.get(u'hl975', u'scrolltext'))

        # After load complete - check config and report. This ensures
        # an error message is left on top of status stack. This is not
        # always a hard fail and the user should be left to determine
        # an appropriate outcome.
        cid = cr.get(u'hl975', u'id')
        if cid and cid != APP_ID:
            self.log.error(u'Meet configuration mismatch: '
                           + repr(cid) + u' != ' + repr(ROADMEET_ID))

    def __init__(self, configpath=None):
        """App constructor."""
        # logger and log handler
        self.log = logging.getLogger()
        self.log.setLevel(logging.DEBUG)
        self.loghandler = None	# set in loadconfig to meet dir

        # meet configuration path and options
        if configpath is None:
            configpath = u'.'	# None assumes 'current dir'
        self.configpath = configpath
        self.loglevel = logging.INFO	# UI log window
        self.dosave = False

        # hardware connections
        self.remote = telegraph.telegraph()
        self.remoteuser = u''		# match against remote nick
        self.remoteport = u''		# only connect if requested
        self.remotechan = u'#announce'
        self.remote.set_pub_cb(self.remote_cb)
        self.port = u''			# re-set in loadconfig
        self.scb = None
        self.trig = None
        self.remote_enable = True
        self.obuf = []			# current output buffer
        self.lbuf = []			# previous output
        for j in range(0,8):
            self.obuf.append(u''.ljust(8))
            self.lbuf.append(u'01234567')
   
        #b = gtk.Builder()
        #b.add_from_file(os.path.join(metarace.UI_PATH, u'hl975.ui'))
        #self.window = b.get_object('appwin')
        #self.status = b.get_object('status')
        self.brightness = 0x31
        #self.line0 = b.get_object('line0')
        #self.line1 = b.get_object('line1')
        #self.scrolltext = b.get_object('scrolltext')
        self.scrolltxt = u''
        #self.scrolltext.grab_focus()
        #self.but_remote = b.get_object('but_remote')
        #for l in [self.line0, self.line1]:
            #l.modify_font(pango.FontDescription('unifont 24'))
            #l.modify_font(pango.FontDescription('monospace bold 24'))
        #self.context = self.status.get_context_id('metarace hl975')
        #b.connect_signals(self)
        self.set_remote_enable()

        # run state
        self.running = True
        self.started = False
        self.vfont = None
        self.vlfont = None
        self.logo = mrlogobmp.METARACE
        self.logofile = None
        self.tod = tod.tod(u'now').truncate(0)
        self.nc = self.tod + tod.tod(u'1.22') # set interval a little off mark
        self.maxlaptime = tod.tod('2:00') # default maximum lap time

        # animation variables
        self.elapstart = None
        self.elapfin = None
        self.finstr = None
        self.timerstat = u'running'	# default assume run state
        self.distance = None
        self.laplbl = None
        self.laptype = None
        self.lapstart = None
        self.lapfin = None
        self.ttrank = None
        self.ttno = None
        self.ttname = None
        self.ttcat = None
        self.tttime = None
        self.timeofday = True  # show timeofday on bottom line?
        self.failcount = 0
        self.failthresh = 30    # connect timeout ~30sec

        # format and connect status handlers
        #f = logging.Formatter('%(levelname)s:%(name)s: %(message)s')
        #self.sh = loghandler.statusHandler(self.status, self.context)
        #self.sh.setLevel(logging.INFO)	# show info+ on status bar
        #self.sh.setFormatter(f)
        #self.log.addHandler(self.sh)

        # start timer
        self.log.debug(u'Starting clock intervals at: ' + self.nc.rawtime(3))
        glib.timeout_add(2000, self.timeout)

def main():
    """Run the road meet application."""
    configpath = None

    # expand configpath on cmd line to realpath _before_ doing chdir
    if len(sys.argv) > 2:
        print(u'usage: hl975 [configdir]\n')
        sys.exit(1)
    elif len(sys.argv) == 2:
        rdir = sys.argv[1]
        if not os.path.isdir(rdir):
            rdir = os.path.dirname(rdir)
        configpath = os.path.realpath(rdir)

    metarace.init()
    if configpath is not None:
        os.chdir(configpath)
    app = hl975(configpath)
    app.loadconfig()
    #app.window.show()
    app.start()
    try:
        metarace.mainloop()
    except:
        app.shutdown(u'Exception from main loop.')
        raise

if __name__ == '__main__':
    main()

