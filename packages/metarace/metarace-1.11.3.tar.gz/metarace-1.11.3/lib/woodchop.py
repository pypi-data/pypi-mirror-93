
# Metarace : Cycle Race Abstractions
# Copyright (C) 2015  Nathan Fraser
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

"""Stihl TIMBERSPORTS timing."""

import pygtk
pygtk.require("2.0")

import gtk
import glib
import gobject
import os
import sys
import time
import logging
import logging.handlers
import serial
import pango

import metarace

from metarace import jsonconfig
from metarace import tod
from metarace import timy
from metarace import ucsv
from metarace import strops
from metarace import loghandler
from metarace import uiutil
from metarace import auplay

LOGFILE = u'woodchop.log'
LOGHANDLER_LEVEL = logging.DEBUG
CONFIGFILE = u'woodchop.json'
WOODCHOP_ID = u'woodchop_1.1'	# configuration versioning

ENCODING = 'iso8859-15'		# scb encoding (not correct but safe)
HL975_BAUD = 9600
EOT=0x04
STX=0x02
ETX=0x03
LF=0x0a
BRIGHTVALS = [0x31, 0x32, 0x33]
IDLESTR = u'        '
TIMERFONT = 'Nimbus Sans L Bold Condensed '
FONTSIZE = 50
EMODES = [u'springboard', u'stocksaw',
          u'standingblock', u'singlebuck',
          u'underhandchop', u'hotsaw']
WINTITLE = u'Stihl TIMBERSPORTS'	# may be set per config

## Model columns
COL_ID = 0
COL_TS = 1
COL_START = 2
COL_AID = 3
COL_A1 = 4
COL_A2 = 5
COL_A3 = 6
COL_BID = 7
COL_B1 = 8
COL_B2 = 9
COL_B3 = 10
COL_WIN = 11
COL_ART = 12
COL_BRT = 13
COL_LOG = 14

class woodchop:
    def menu_quit_cb(self, menuitem, data=None):
        """Quit the application."""
        self.running = False
        self.window.destroy()

    def menu_reset_cb(self, menuitem, data=None):
        """Reset from menu bar."""
        self.resettime()

    def resettime(self):
        if self.scb is not None:
            self.scb.setDTR(False)
        self.timerstat = u'idle'
        uiutil.buttonchg(self.runctrl, uiutil.bg_none, 'Idle')
        self.atime.set_text(IDLESTR)
        self.aentry.set_text(u'')
        self.btime.set_text(IDLESTR)
        self.bentry.set_text(u'')
        self.player.stop()
        self.lstart = None
        self.tstart = None
        for c in [2,3,4,5,6,7]:
            self.timer.dearm(c)
        self.timer.armlock(False)
        self.timer.arm(0)
        self.runid = None
        self.atimes = {1:None,2:None,3:None}
        self.btimes = {1:None,2:None,3:None}
        self.setline(0,IDLESTR)
        self.setline(1,IDLESTR)

    def refresh_display(self, data=None):
        self.oline[0] = u''
        self.oline[1] = u''
        return False	# for timeout

    def starttrig(self, t):
        if self.timerstat == u'idle':
            if self.scb is not None:
                self.scb.setDTR(True)
            self.timerstat = u'ready'
            self.log.info(u'Start Trigger')
            if t.ltime is not None:
                self.lstart = tod.tod(t.ltime) + self.stoft
            else:
                self.lstart = tod.tod(u'now') + self.stoft
            self.tstart = t + self.stoft
            self.player.play()
            self.atime.set_text(u'        ')
            self.btime.set_text(u'        ')
            uiutil.buttonchg(self.runctrl, uiutil.bg_armint, 'Ready')
        else:
            self.log.debug(u'Spurious Start Trigger')

    def addrow(self):
        """Add a new row for the current run and return the run id."""
        nextid = len(self.model) + 1
        timestamp = time.asctime()
        logstr = u''
        nr = [str(nextid),timestamp, tod.ZERO,
              self.aentry.get_text(), None, None, None,
              self.bentry.get_text(), None, None, None,
              u'',None,None,logstr]
        self.model.append(nr)
        return nextid

    def register_time(self, t):
        """Transfer a time into model - also handling the allocations."""
        if self.runid is None:
            # allocate a new run for this result
            self.runid = self.addrow()
        r = self.model[self.runid - 1]
        # update any strings
        r[COL_AID] = self.aentry.get_text()
        r[COL_BID] = self.bentry.get_text()
        chan = timy.chan2id(t.chan)
        if chan == 2:	# A1
            self.atimes[1] = (t-self.tstart).truncate(2)
            r[COL_A1] = self.atimes[1]
            r[COL_LOG] += u'A1: ' + self.atimes[1].rawtime(2) + u'\n'
        elif chan == 4: # A2 
            self.atimes[2] = (t-self.tstart).truncate(2)
            r[COL_A2] = self.atimes[2]
            r[COL_LOG] += u'A2: ' + self.atimes[2].rawtime(2) + u'\n'
        elif chan == 6: # A3 
            self.atimes[3] = (t-self.tstart).truncate(2)
            r[COL_A3] = self.atimes[3]
            r[COL_LOG] += u'A3: ' + self.atimes[3].rawtime(2) + u'\n'
        elif chan == 3: # B1 
            self.btimes[1] = (t-self.tstart).truncate(2)
            r[COL_B1] = self.btimes[1]
            r[COL_LOG] += u'B1: ' + self.btimes[1].rawtime(2) + u'\n'
        elif chan == 5: # B2 
            self.btimes[2] = (t-self.tstart).truncate(2)
            r[COL_B2] = self.btimes[2]
            r[COL_LOG] += u'B2: ' + self.btimes[2].rawtime(2) + u'\n'
        elif chan == 7: # B3 
            self.btimes[3] = (t-self.tstart).truncate(2)
            r[COL_B3] = self.btimes[3]
            r[COL_LOG] += u'B3: ' + self.btimes[3].rawtime(2) + u'\n'
        glib.idle_add(self.recalculate)
        
    def timercb(self, e):
        """Handle a timer event."""
        chan = timy.chan2id(e.chan)
        if chan == timy.CHAN_START:
            if self.tstart is None:
                self.starttrig(e)
                self.log.debug('Got a start impulse.')
            else:
                self.log.debug(u'Spurious start trigger.')
        elif self.tstart is not None and self.timerstat != u'finished':
            self.register_time(e)
        else:
            self.log.debug(u'Spurious timer impulse: ' + unicode(e))
        return False

    def menu_about_cb(self, menuitem, data=None):
        """Display metarace about dialog."""
        dlg = gtk.AboutDialog()
        dlg.set_transient_for(self.window)
        dlg.set_name(u'woodchop')
        dlg.set_version(metarace.VERSION)
        dlg.set_copyright(u'Copyright \u00a9 2015 Nathan Fraser')
        dlg.set_comments(u'For Stihl TIMBERSPORTS')
        dlg.set_website(u'http://metarace.com.au/')
        dlg.set_license(metarace.LICENSETEXT)
        dlg.run()
        dlg.destroy()
  
    def torunning(self):
        """Move status to running/capture."""
        #if self.scb is not None:
            #self.scb.setDTR(True)
        self.timerstat = u'running'
        self.timer.armlock(True)
        for c in [2,3,4,5,6,7]:
            self.timer.arm(c)
        uiutil.buttonchg(self.runctrl, uiutil.bg_armstart, 'Running')

    def tofinished(self):
        """Set finished status and disable capture."""
        for c in [2,3,4,5,6,7]:
            self.timer.dearm(c)
        self.timer.armlock(False)
        self.timerstat = u'finished'
        uiutil.buttonchg(self.runctrl, uiutil.bg_none, 'Finished')
    
    def timeout(self):
        """Update internal state and re-display."""
        if not self.running:
            return False		# termination
        try:
            astr = IDLESTR
            bstr = IDLESTR
            nowtime = tod.tod(u'now')
            if self.timerstat in [u'ready', u'running', u'finished']:
                astr = u'    -.- '
                bstr = u'    -.- '
                if nowtime > self.lstart:
                    # rolling time
                    rtstr = strops.truncpad(
                              (nowtime - self.lstart).rawtime(1) + u' ',
                               7,align='r',elipsis=False)
                    astr = u' ' + rtstr
                    bstr = u' ' + rtstr
                    ao = False
                    bo = False
                    if self.timerstat == u'ready':
                        self.torunning()
                    # check for completion in one or both lanes
                    theastr = u''
                    theatime = self.runtime(self.atimes[1],
                                            self.atimes[2],
                                            self.atimes[3],
                                            self.mintimes)
                    if theatime is not None:
                        theastr = strops.truncpad(theatime.rawtime(2),7,
                                                  align='r',elipsis=False)
                        ao = True
                    thebstr = u''
                    thebtime = self.runtime(self.btimes[1],
                                            self.btimes[2],
                                            self.btimes[3],
                                            self.mintimes)
                    if thebtime is not None:
                        thebstr = strops.truncpad(thebtime.rawtime(2),7,
                                                  align='r',elipsis=False)
                        bo = True
                    ares = u' '
                    bres = u' '
                    if ao and bo:
                        if theatime < thebtime:
                            ares = u'*'
                        elif theatime == thebtime:
                            ares = u'*'
                            bres = u'*'
                        else:
                            bres = u'*'
                    elif ao:
                        ares = u'*'
                    elif bo:
                        bres = u'*'
                    if theastr:
                        # overwrite a str
                        astr = ares + theastr
                    if thebstr:
                        # overwrite b str
                        bstr = bres + thebstr
                else:	# waiting for start
                    astr = u'        '
                    bstr = u'        '
                # write to boards
                if self.atimeron:
                    self.atime.set_text(astr)
                else:
                    astr = IDLESTR
                if self.btimeron:
                    self.btime.set_text(bstr)
                else:
                    bstr = IDLESTR
            else:
                pass
            # always update the a and b str 
            self.setline(0,astr)
            self.setline(1,bstr)
        except Exception as e:
            self.log.error(u'Timeout: ' + unicode(e))
        return True

    def emode_0_toggled_cb(self, button, data=None):
        """Handle toggle on mode 0."""
        self.log.debug(u'Mode 0 toggled.')
        curstate = button.get_active()
        if curstate:
            self.log.info(u'Event set to: Springboard.')
            self.emode = u'springboard'
            self.set_playfile()

    def emode_1_toggled_cb(self, button, data=None):
        """Handle toggle on mode 1."""
        self.log.debug(u'Mode 1 toggled.')
        curstate = button.get_active()
        if curstate:
            self.log.info(u'Event set to: Stock Saw.')
            self.emode = u'stocksaw'
            self.set_playfile()

    def emode_2_toggled_cb(self, button, data=None):
        """Handle toggle on mode 2."""
        self.log.debug(u'Mode 2 toggled.')
        curstate = button.get_active()
        if curstate:
            self.log.info(u'Event set to: Standing Block.')
            self.emode = u'standingblock'
            self.set_playfile()

    def emode_3_toggled_cb(self, button, data=None):
        """Handle toggle on mode 3."""
        self.log.debug(u'Mode 3 toggled.')
        curstate = button.get_active()
        if curstate:
            self.log.info(u'Event set to: Single Buck.')
            self.emode = u'singlebuck'
            self.set_playfile()

    def emode_4_toggled_cb(self, button, data=None):
        """Handle toggle on mode 4."""
        self.log.debug(u'Mode 4 toggled.')
        curstate = button.get_active()
        if curstate:
            self.log.info(u'Event set to: Underhand Chop.')
            self.emode = u'underhand'
            self.set_playfile()

    def emode_5_toggled_cb(self, button, data=None):
        """Handle toggle on mode 5."""
        self.log.debug(u'Mode 5 toggled.')
        curstate = button.get_active()
        if curstate:
            self.log.info(u'Event set to: Hot Saw.')
            self.emode = u'hotsaw'
            self.set_playfile()
 
    def aenable_toggled_cb(self, button, data=None):
        """Handle toggle A timer enable."""
        self.log.debug(u'A Timer Toggled.')
        curstate = button.get_active()
        if curstate:
            self.log.info(u'Enable A Timer')
        else:
            self.log.info(u'Disable A Timer')
            self.atime.set_text(IDLESTR)
            self.setline(0,IDLESTR)
        self.atimeron = curstate	# may happen twice - but that's ok

    def benable_toggled_cb(self, button, data=None):
        """Handle toggle B timer enable."""
        self.log.debug(u'B Timer Toggled.')
        curstate = button.get_active()
        if curstate:
            self.log.info(u'Enable B Timer')
        else:
            self.log.info(u'Disable B Timer')
            self.btime.set_text(IDLESTR)
            self.setline(1,IDLESTR)
        self.btimeron = curstate	# may happen twice - but that's ok

    def menu_display_cb(self, menuitem, data=None):
        """Run a display test procedure."""
        self.log.debug(u'Display test.')
        msg = u'-LINE A-'
        cmd = (chr(STX) + chr(0x31 + 0) + chr(self.brightness)
                + msg.encode(ENCODING,'replace') + chr(LF))
        self.serialwrite(cmd)
        msg = u'-LINE B-'
        cmd = (chr(STX) + chr(0x31 + 1) + chr(self.brightness)
                + msg.encode(ENCODING,'replace') + chr(LF))
        self.serialwrite(cmd)
        # test duration is 10 sec, but will be cleared on other events
        glib.timeout_add_seconds(10, self.refresh_display)

    def menu_export_cb(self, menuitem, data=None):
        """Export result to csv file."""
        self.log.debug(u'Export.')
        rfilename = uiutil.savecsvdlg(u'Select file to save result to.',
                                       self.window,
                                       u'results.csv', self.configpath)
        if rfilename is not None:
            with open(rfilename , 'wb') as f:
                cw = ucsv.UnicodeWriter(f)
                cw.writerow([u'Run', u'TS', u'A', u'A1', u'A2', u'A3', u'AT',
                                            u'B', u'B1', u'B2', u'B3', u'BT',
                                            u'Res', u'Log'])
                for r in self.model:
                    outrow = [r[COL_ID],r[COL_TS],
                      r[COL_AID], r[COL_A1], r[COL_A2], r[COL_A3], r[COL_ART],
                      r[COL_BID], r[COL_B1], r[COL_B2], r[COL_B3], r[COL_BRT],
                      r[COL_WIN], r[COL_LOG]]
                    for col in [3,4,5,6, 8,9,10,11]:
                        if outrow[col] is not None:
                            outrow[col] = outrow[col].rawtime(2)
                        else:
                            outrow[col] = u''
                    cw.writerow(outrow)
            self.log.info(u'Exported meet results to ' + repr(rfilename))

    def menu_preferences_cb(self, menuitem, data=None):
        """Run a property configuration dialog."""
        self.log.debug(u'Preferences.')
        # not implemented

    def isconfigdefault(self):
        """True if the current working file is a default unnnamed contest."""
        usingfile = os.path.basename(self.configfile)
        return CONFIGFILE == usingfile

    def newfilename(self):
        """Return a timestamped filename only."""
        return u'chop_' + time.strftime(u'%Y%m%d-%H%M%S') + u'.wcd'

    def menu_saveas_cb(self, menuitem, data=None):
        """Handle Save As menu item."""
        self.log.debug(u'Save-As.')
        self.saveconfig()		# always save out
        self.menu_saveas_dlg()		# then maybe choose a new file
        self.log.info(u'Competition saved to '
                      + os.path.basename(self.configfile))

    def menu_saveas_dlg(self):
        """Choose a new file to save to."""
        dlg = gtk.FileChooserDialog(u'Choose filename to save to.',
                                        self.window,
                    gtk.FILE_CHOOSER_ACTION_SAVE, (gtk.STOCK_CANCEL,
                    gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK))
        cfilt = gtk.FileFilter()
        cfilt.set_name('TIMBERSPORTS Config')
        cfilt.add_mime_type('application/json')
        cfilt.add_pattern('*.wcd')
        dlg.add_filter(cfilt)
        cfilt = gtk.FileFilter()
        cfilt.set_name('All Files')
        cfilt.add_pattern("*")
        dlg.add_filter(cfilt)
        dlg.set_current_folder(self.configpath)
        dlg.set_current_name(self.newfilename())
        response = dlg.run()
        if response == gtk.RESPONSE_OK:
            self.configfile = dlg.get_filename().decode('utf-8')
            winstr = self.wintitle + u' (' + os.path.basename(self.configfile) + u')'
            self.saveconfig()
            self.window.set_title(winstr)
        dlg.destroy()

    def menu_save_cb(self, menuitem, data=None):
        """Handle the save menu item."""
        self.log.debug(u'Save.')
        self.saveconfig()		# always save out
        if self.isconfigdefault():	# but also choose if using default
            self.menu_saveas_dlg()
        self.log.info(u'Competition saved to '
                      + os.path.basename(self.configfile))

    def menu_open_cb(self, menuitem, data=None):
        """Handle the open menu item."""
        self.log.debug(u'Open.')
        # save a backup of the current working config
        if self.isconfigdefault():
            self.configfile = os.path.join(self.configpath,
                                           self.newfilename())
        self.saveconfig()

        # choose config to load from
        dlg = gtk.FileChooserDialog(u'Load a previously saved contest.',
                                    self.window,
                       gtk.FILE_CHOOSER_ACTION_OPEN, (gtk.STOCK_CANCEL,
                       gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        cfilt = gtk.FileFilter()
        cfilt.set_name('TIMBERSPORTS Config')
        cfilt.add_mime_type('application/json')
        cfilt.add_pattern('*.wcd')
        dlg.add_filter(cfilt)
        cfilt = gtk.FileFilter()
        cfilt.set_name('All Files')
        cfilt.add_pattern("*")
        dlg.add_filter(cfilt)
        dlg.set_current_folder(self.configpath)
        response = dlg.run()
        if response == gtk.RESPONSE_OK:
            # clear out current result
            self.model.clear()
            self.runid = None
            newfile = dlg.get_filename().decode('utf-8')
            self.configfile = newfile
            self.loadconfig(newfile)
            self.log.info(u'Loaded competition from: ' + newfile)
        dlg.destroy()

        # call into recalc
        self.recalculate()

    def menu_new_cb(self, menuitem, data=None):
        """Handle new menu item."""
        self.log.debug(u'New.')
        if not uiutil.questiondlg(self.window,
                 u'Clear results and start a new contest?'):
            return False
        if self.isconfigdefault():
            self.configfile = os.path.join(self.configpath,
                                           self.newfilename())
        self.log.info(u'Previous contest saved to: '
                      + os.path.basename(self.configfile))
        self.saveconfig()
        self.configfile = os.path.join(self.default_config())
        self.window.set_title(self.wintitle)
        # clear out all runs and call into recalc
        self.model.clear()
        self.runid = None
        self.recalculate()

    def destroy_cb(self, window, msg=u''):
        """Handle destroy signal and exit application."""
        if self.started:
            self.saveconfig()
            deffile = self.default_config()
            if deffile != self.configfile:
                # if the active file is not default, also save to default
                self.log.debug(u'Save file is not default: '
                        + repr(deffile) + u' != ' + repr(self.configfile))
                self.saveconfig(deffile)
            self.log.info(u'Shutdown: ' + msg)
            self.shutdown(msg)
        self.log.removeHandler(self.sh)
        if self.loghandler is not None:
            self.log.removeHandler(self.loghandler)
        metarace.unlockpath(self.configpath)
        self.running = False
        gtk.main_quit()
        print(u'Exit.')

    def key_event(self, widget, event):
        """Collect key events on main window and send to race."""
        if event.type == gtk.gdk.KEY_PRESS:
            key = gtk.gdk.keyval_name(event.keyval) or 'None'
            # Switch on CTRL
            if event.state & gtk.gdk.CONTROL_MASK:
                # Handle special fake timer keys
                if key in ['0','1','2','3','4','5','6','7','8','9']:	#?uni
                    self.timer.trig(chan=key)
                    return True
            else:
                pass
        return False

    def connect_display(self):
        """Connect to display serial port."""
        self.close_display()
        self.log.debug(u'Connecting serial port: ' + repr(self.scbport))
        try:
            self.scb = serial.Serial(self.scbport, HL975_BAUD, timeout=0.2)
            self.setline(0,u'A       ')
            self.setline(1,u'B       ')
        except Exception as e:
            self.log.error(u'Opening serial port: ' + repr(e))
            self.scb = None

    def close_display(self):
        """Close serial port."""
        if self.scb is not None:
            self.log.info(u'Closing Display.')
            self.scb.close()    # serial port close
            self.scb = None             # release handle

    def shutdown(self, msg):
        """Cleanly shutdown threads and close application."""
        self.started = False
        self.close_display()
        self.player.exit(msg)
        self.timer.exit(msg)
        print (u'Waiting for timer...')
        self.player.join()
        self.timer.join()

    def start(self):
        """Start the timer and scoreboard threads."""
        if not self.started:
            self.log.debug(u'Woodchop startup.')
            if not metarace.lockpath(self.configpath):
                self.log.error('Unable to get lock on configpath.')
                dlg = gtk.MessageDialog(self.window, gtk.DIALOG_MODAL,
                                        gtk.MESSAGE_INFO, gtk.BUTTONS_OK,
                                        u'Program already running.')
                dlg.format_secondary_text(
           u'Another instance of the program appears to be running already.')
                dlg.run()
                dlg.destroy()
                raise(Exception('Unable to get lock on configpath.'))
            self.timer.start()
            self.player.start()
            self.started = True

    def editcol_db(self, cell, path, new_text, col):
        """Cell update."""
        new_text = new_text.strip()
        self.model[path][col] = new_text.strip()

    def showtod_cb(self, col, cr, model, iter, modelcol=None):
        """Draw tod in view."""
        st = model.get_value(iter, modelcol)
        otxt = ''
        if st is not None:
            otxt = st.rawtime(2)
        else:
            pass
        cr.set_property('text', otxt)

    def edittod_cb(self, cell, path, new_text, modelcol=None):
        """Edit tod on rider view."""
        newst = tod.str2tod(new_text)
        self.model[path][modelcol] = newst
        glib.idle_add(self.recalculate)

    def runtime(self, t1, t2, t3, mintimes=1):
        """Determine run time from provided."""
        ret = None
        tv = []
        for t in [t1, t2, t3]:
            if t is not None:
                tv.append(t)
        if len(tv) == 1 and 1 >= mintimes:
            ret = tv[0]
        elif len(tv) == 3:
            tv.sort()
            ret = tv[1]
        elif len(tv) == 2 and 2 >= mintimes:
            # average
            ret = tod.tod(str(0.5 * 
                              (float(tv[0].timeval) 
                               + float(tv[1].timeval)))).truncate(2)
        else:
            pass
        return ret
        
    def recalculate(self):
        """Update all model winners."""
        self.log.debug(u'Recalculate')
        for r in self.model:
            art = self.runtime(r[COL_A1],r[COL_A2],r[COL_A3])
            r[COL_ART] = art
            brt = self.runtime(r[COL_B1],r[COL_B2],r[COL_B3])
            r[COL_BRT] = brt
            if art is not None and brt is not None:
                if art < brt:
                    r[COL_WIN] = u'A'
                elif art == brt:
                    r[COL_WIN] = u'='
                else:
                    r[COL_WIN] = u'B'
            else:
                if art is not None:
                    r[COL_WIN] = u'A'
                elif brt is not None:
                    r[COL_WIN] = u'B'
                else:
                    r[COL_WIN] = u''
        self.saveconfig()

    def runctrl_clicked_cb(self, button, data=None):
        """Respond to click on ctrl button."""
        if self.timerstat in [u'running']:
            self.tofinished()
        elif self.timerstat in [u'finished']:
            self.resettime()
        else:
            self.log.debug(u'ctrl clicked with no outcome.')

    def serialwrite(self, cmd):
        """Output command blocking."""
        try:
            if self.scb:
                self.scb.write(cmd)
        except Exception as e:
            self.log.error(u'Writing to scoreboard: ' + repr(e))

    def setline(self, line, msg=u'        '):
        """Copy line to display."""
        if self.oline[line] != msg:
            cmd = (chr(STX) + chr(0x31 + line) + chr(self.brightness)
                + msg.encode(ENCODING,'replace') + chr(LF))
            self.log.debug(u'Writing to line '
                           + repr(line) + ' :: ' + repr(cmd))
            self.serialwrite(cmd)
            self.oline[line] = msg

    def saveconfig(self, altfile=None):
        """Save current data to disk."""
        configfile = self.configfile
        if altfile is not None:
            configfile = altfile
        cw = jsonconfig.config()
        cw.add_section(u'woodchop')
        cw.set(u'woodchop', u'id', WOODCHOP_ID)
        cw.set(u'woodchop', u'timer', self.timer_port)
        cw.set(u'woodchop', u'configfile', self.configfile)
        cw.set(u'woodchop', u'brightness', self.brightness)
        cw.set(u'woodchop', u'atimeron', self.atimeron)
        cw.set(u'woodchop', u'btimeron', self.btimeron)
        cw.set(u'woodchop', u'fontsize', self.fontsize)
        cw.set(u'woodchop', u'scbport', self.scbport)
        cw.set(u'woodchop', u'cadstoft', self.cadstoft.rawtime(2))
        cw.set(u'woodchop', u'gunstoft', self.gunstoft.rawtime(2))
        cw.set(u'woodchop', u'emode', self.emode)
        cw.set(u'woodchop', u'mintimes', self.mintimes)

        # save runs
        runout = []
        for r in self.model:
            nr = list(r)	# copy content to new list
            for col in [COL_START,
                        COL_A1, COL_A2, COL_A3,
                        COL_B1, COL_B2, COL_B3,
                        COL_ART, COL_BRT]:
                if nr[col] is not None:
                    nr[col] = nr[col].rawtime()	# convert to str
                else:
                    nr[col] = u''	# empty tod
            runout.append(nr)

        cw.set(u'woodchop', u'runs', runout)
        self.log.debug(u'Saving config to ' + repr(configfile))
        with open(configfile, 'wb') as f:
            cw.write(f)

    def set_timerfont(self):
        """Update the display from current settings."""
        fnt = pango.FontDescription(TIMERFONT + str(self.fontsize))
        self.atime.modify_font(fnt)
        self.btime.modify_font(fnt)

    def default_config(self, cffile=CONFIGFILE):
        return os.path.join(self.configpath, cffile)

    def loadconfig(self, altconfig=None):
        """Load config from disk."""
        # note uses an absolute path - for comparison with configfile
        cr = jsonconfig.config({u'woodchop':{u'timer':u'/dev/ttyUSB0',
                                        u'scbport':u'/dev/ttyUSB1',
                                        u'configfile':self.configfile,
                                        u'atimeron':True,
                                        u'btimeron':True,
                                        u'mintimes': 2,
                                        u'fontsize':FONTSIZE,
                                        u'stfile':u'woodchop.wav',
                                        u'cadstoft': u'3.70',
                                        u'gunstfile':u'woodchop_gunstart.wav',
                                        u'gunstoft': u'0.0',
                                        u'brightness': 0x31,
                                        u'emode': u'springboard',
                                        u'runs': [],
                                        u'wintitle': WINTITLE,
                                        u'id':u''}})
        cr.add_section(u'woodchop')
        cr.merge(metarace.sysconf, u'woodchop')
        cffile = self.configfile
        if altconfig is not None:
            cffile = altconfig

        # check for config file
        try:
            with open(cffile, 'rb') as f:
                self.log.debug(u'Loading from: ' + repr(cffile))
                cr.read(f)
        except Exception as e:
            self.log.error(u'Reading config: ' + unicode(e))

        # check for recurse, only if starting with a default config
        usingfile = os.path.basename(cffile)
        newcf = cr.get(u'woodchop', u'configfile')
        namedfile = os.path.basename(newcf)
        if CONFIGFILE == usingfile and usingfile != namedfile:
            self.log.debug(u'Recurse: Read file is not same as current file '
                           + repr(usingfile) + u' != ' + repr(namedfile))
            # load from other file
            self.configfile = newcf
            return self.loadconfig(newcf)

        # set main timer port (always re-connect)
        nport = cr.get(u'woodchop', u'timer')
        self.timer_port = nport
        self.timer.setport(nport)
        self.timer.sane()
        self.timer.delaytime(0.4)
        self.timer.write('BE0')
        self.timer.setcb(self.timercb)
        self.brightness = strops.confopt_posint(cr.get(u'woodchop',
                                                       u'brightness'))
        self.aenable.set_active(strops.confopt_bool(cr.get(u'woodchop',
                                                           u'atimeron')))
        self.benable.set_active(strops.confopt_bool(cr.get(u'woodchop',
                                                           u'btimeron')))

        # adjust timer font size
        self.fontsize = strops.confopt_posint(cr.get(u'woodchop',
                                                     u'fontsize'), FONTSIZE)
        self.set_timerfont()

        # set scb port
        self.scbport = cr.get(u'woodchop', u'scbport')
        self.connect_display()

        # set audio files and positions
        self.stfile = cr.get(u'woodchop', u'stfile')
        self.cadstoft = tod.str2tod(cr.get(u'woodchop', u'cadstoft'))
        if self.cadstoft is None:
            self.cadstoft = tod.tod(u'3.70')	# failsafe
        self.gunstfile = cr.get(u'woodchop', u'gunstfile')
        self.gunstoft = tod.str2tod(cr.get(u'woodchop', u'gunstoft'))
        if self.gunstoft is None:
            self.gunstoft = tod.tod(u'0.1')	# failsafe
        self.set_playfile()	# also sets stoft

        # runtimes
        self.mintimes = strops.confopt_posint(cr.get(u'woodchop', u'mintimes'),
                                              2)

        # load runs
        for run in cr.get(u'woodchop', u'runs'):
            if type(run) is list and len(run) > 14:	# ignore invalid len
                for col in [COL_START, COL_A1, COL_A2, COL_A3,
                                       COL_B1, COL_B2, COL_B3,
                                       COL_ART, COL_BRT]:
                    run[col] = tod.str2tod(run[col])	# conv to tod
                self.model.append(run) 
            else:
                self.log.error(u'Invalid row in run data: ' + repr(run))

        # fetch event mode (sorry)
        nemode = strops.confopt_list(cr.get(u'woodchop', u'emode'),
                                     EMODES,
                                     u'springboard')
        if nemode == EMODES[0]:
            self.emode0.set_active(True)
        elif nemode == EMODES[1]:
            self.emode1.set_active(True)
        elif nemode == EMODES[2]:
            self.emode2.set_active(True)
        elif nemode == EMODES[3]:
            self.emode3.set_active(True)
        elif nemode == EMODES[4]:
            self.emode4.set_active(True)
        elif nemode == EMODES[5]:
            self.emode5.set_active(True)
        else:
            self.log.debug(u'Unknown emode error: ' + repr(nemode))
            self.emode0.set_active(True)

        # Set window title
        self.wintitle = cr.get(u'woodchop', u'wintitle')
        winstr = self.wintitle
        if CONFIGFILE != usingfile:
            winstr += u' (' + usingfile + u')'
        self.window.set_title(winstr)
        # After load complete - check config and report.
        cid = cr.get(u'woodchop', u'id')
        if cid != WOODCHOP_ID:
            self.log.error(u'Configuration ID mismatch: '
                           + repr(cid) + u' != ' + repr(WOODCHOP_ID))

        self.resettime()
        return False

    def set_playfile(self):
        """Check config for current mode and then set the playfile."""
        sndfile = self.stfile
        self.stoft = self.cadstoft
        if self.emode in [u'stocksaw',u'hotsaw']:
            sndfile = self.gunstfile
            self.stoft = self.gunstoft
        self.player.setfile(metarace.default_file(sndfile))
        
    def __init__(self, configpath=None):
        """Constructor."""
        # meet configuration path and options
        if configpath is None:
            configpath = u'.'	# None assumes 'current dir'
        self.configpath = configpath
        self.configfile = self.default_config()

        # re-set log handling
        self.log = logging.getLogger()
        self.log.setLevel(logging.DEBUG)
        self.loghandler = logging.handlers.RotatingFileHandler(
                             os.path.join(self.configpath, LOGFILE),
                             maxBytes=2097152,
                             backupCount=2)
        self.loghandler.setLevel(LOGHANDLER_LEVEL)
        self.loghandler.setFormatter(logging.Formatter(metarace.LOGFORMAT))
        self.log.addHandler(self.loghandler)

        self.timer = timy.timy(u'', name=u'main')
        self.timer_port = u''
        self.scb = None
        self.scbport = u''
        self.oline = [u'',u'']	# scb line output buffer
        self.brightness = 0x31
        self.fontsize = FONTSIZE

        # Audio output
        self.player = auplay.auplay()

        self.emode = u'springboard'
        self.stfile = None
        self.stoft = None
        self.gunstfile = None
        self.gunstoft = None
        self.curstoft = None
        self.wintitle = u''

        # runtime
        self.chopmode = None
        self.timerstat = u'idle'
        self.lstart = None
        self.tstart = None
        self.runid = None
        self.atimes = {1:None,2:None,3:None}
        self.btimes = {1:None,2:None,3:None}
        self.mintimes = 2

        # UI
        b = gtk.Builder()
        b.add_from_file(os.path.join(metarace.UI_PATH, u'woodchop.ui'))
        self.window = b.get_object('window')
        self.window.connect('key-press-event', self.key_event)
        self.status = b.get_object('statusbar')
        self.context = self.status.get_context_id('metarace woodchop')
        self.resultwin = b.get_object('resultwin')
        self.aentry = b.get_object('aentry')
        self.bentry = b.get_object('bentry')
        self.aenable = b.get_object('aenable')
        self.benable = b.get_object('benable')
        self.emode0 = b.get_object('emode_0')
        self.emode1 = b.get_object('emode_1')
        self.emode2 = b.get_object('emode_2')
        self.emode3 = b.get_object('emode_3')
        self.emode4 = b.get_object('emode_4')
        self.emode5 = b.get_object('emode_5')
        self.atimeron = True
        self.atime = b.get_object('atime')
        self.btimeron = True
        self.btime = b.get_object('btime')
        self.set_timerfont()
        self.atime.set_text(u'A  --.- ')
        self.btime.set_text(u'B  --.- ')
        self.runctrl = b.get_object('runctrl')
        b.connect_signals(self)

        # tree model
        self.model = gtk.ListStore(gobject.TYPE_STRING, # COL_ID = 0
                                   gobject.TYPE_STRING, # COL_TS = 1
                                   gobject.TYPE_PYOBJECT, # COL_START = 2
                                   gobject.TYPE_STRING, # COL_AID = 3
                                   gobject.TYPE_PYOBJECT, # COL_A1 = 4
                                   gobject.TYPE_PYOBJECT, # COL_A2 = 5
                                   gobject.TYPE_PYOBJECT, # COL_A3 = 6
                                   gobject.TYPE_STRING, # COL_BID = 7
                                   gobject.TYPE_PYOBJECT, # COL_B1 = 8
                                   gobject.TYPE_PYOBJECT, # COL_B2 = 9
                                   gobject.TYPE_PYOBJECT, # COL_B3 =10 
                                   gobject.TYPE_STRING,  # COL_WIN = 11
                                   gobject.TYPE_PYOBJECT, # COL_ART =12 
                                   gobject.TYPE_PYOBJECT, # COL_BRT =13 
                                   gobject.TYPE_STRING) # COL_LOG =14

        t = gtk.TreeView(self.model)
        self.view = t
        t.set_reorderable(True)
        t.set_rules_hint(True)
        uiutil.mkviewcoltxt(t, 'Run', COL_ID, calign=0.0)
        uiutil.mkviewcoltxt(t, 'A', COL_AID,
                               self.editcol_db, expand=True)
        uiutil.mkviewcoltod(t, '1', cb=self.showtod_cb, width=75,
                                editcb=self.edittod_cb, colno=COL_A1)
        uiutil.mkviewcoltod(t, '2', cb=self.showtod_cb, width=75,
                                editcb=self.edittod_cb, colno=COL_A2)
        uiutil.mkviewcoltod(t, '3', cb=self.showtod_cb, width=75,
                                editcb=self.edittod_cb, colno=COL_A3)
        uiutil.mkviewcoltod(t, 'RT', cb=self.showtod_cb, width=75,
                                colno=COL_ART)
        uiutil.mkviewcoltxt(t, 'B', COL_BID,
                               self.editcol_db, expand=True)
        uiutil.mkviewcoltod(t, '1', cb=self.showtod_cb, width=75,
                                editcb=self.edittod_cb, colno=COL_B1)
        uiutil.mkviewcoltod(t, '2', cb=self.showtod_cb, width=75,
                                editcb=self.edittod_cb, colno=COL_B2)
        uiutil.mkviewcoltod(t, '3', cb=self.showtod_cb, width=75,
                                editcb=self.edittod_cb, colno=COL_B3)
        uiutil.mkviewcoltod(t, 'RT', cb=self.showtod_cb, width=75,
                                colno=COL_BRT)
        uiutil.mkviewcoltxt(t, 'Win', COL_WIN)
        t.show()
        self.resultwin.add(t)

        # run state
        self.running = True
        self.started = False

        # format and connect status and log handlers
        f = logging.Formatter('%(levelname)s:%(name)s: %(message)s')
        self.sh = loghandler.statusHandler(self.status, self.context)
        self.sh.setLevel(logging.INFO)	# show info upon status bar
        self.sh.setFormatter(f)
        self.log.addHandler(self.sh)
        self.sh.setLevel(logging.INFO)	# show info upon status bar

        # start timer ~ 0.05s
        glib.timeout_add(50, self.timeout)
        self.window.maximize()

def main():
    """Run the application."""
    configpath = None
    # expand config on cmd line to realpath _before_ doing chdir
    if len(sys.argv) > 2:
        print(u'usage: woodchop [configdir]\n')
        sys.exit(1)
    elif len(sys.argv) == 2:
        configpath = os.path.realpath(os.path.dirname(sys.argv[1]))

    metarace.init()
    app = woodchop(configpath)
    app.loadconfig()
    app.window.show()
    app.start()
    try:
        metarace.mainloop()
    except:
        app.shutdown(u'Exception from main loop.')
        raise

if __name__ == '__main__':
    main()
