
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

import pygtk
pygtk.require("2.0")

import gtk
import glib
import pango
import pangocairo
import logging
import os
import sys
import serial

import metarace
from metarace import tod
from metarace import timy
from metarace import telegraph
from metarace import strops
from metarace import ucsv
from metarace import jsonconfig
from metarace import auplay

LOGFILE=u'trackstart.log'
TIMEFONT='Nimbus Sans L Condensed Bold '
COUNTERFONT='Nimbus Sans L Condensed Bold '
# TYPICAL SYNC ERROR: 17619048	# typical playback error ~20ms
DEFAUDIOSYNCTHRESH = 100000000	# Tolerate no more than 100ms audio desync
				# note: on Pi/ARM, 200ms reqd due to proc lag
                                # this is now configurable
				# NOT USED WITH PYGAME - alternate app reqd
ENCODING = 'iso8859-15'
HL975_BAUD = 9600
EOT=0x04
STX=0x02
ETX=0x03
LF=0x0a
GFXHEAD = bytearray([EOT, EOT, 0x30, 0x47])
BRIGHTVALS = [0x31, 0x32, 0x33]

# squeeze text into a desired width
def fit_cent(cr, pr, oh, ow, msg, ch, fn):
    """squeeze text centered at h."""
    if msg is not None:
        cr.save()
        l = pr.create_layout()
        l.set_font_description(pango.FontDescription(fn + str(ch)))
        l.set_text(msg)
        (tw,th) = l.get_pixel_size()
        if tw > ow:
            cr.scale(float(ow)/float(tw),1.0)
            tw = ow
        cr.move_to(0.5*(ow-tw), oh)
        pr.update_layout(l)
        pr.show_layout(l)
        cr.restore()

# draw text centred
def text_cent(cr, pr, oh, ow, msg, ch, fn):
    """Position text centred at h."""
    if msg is not None:
        cr.save()
        l = pr.create_layout()
        l.set_font_description(pango.FontDescription(fn + str(ch)))
        l.set_text(msg)
        (tw,th) = l.get_pixel_size()
        cr.move_to(ow-(0.5 * tw), oh)
        pr.update_layout(l)
        pr.show_layout(l)
        cr.restore()

def tod2key(tod=None):
    """Return a key from the supplied time of day."""
    ret = None
    if tod is not None:
        ret = int(tod.truncate(0).timeval)
    return ret

class countdown(object):
    """Start Display application."""
 
    def setcdn(self,cnt=None):
        """Copy line to display."""
        line = u'        '
        if cnt is not None:
            line = strops.truncpad(unicode(cnt),2,align='r')+u'      '
        cmd = (chr(STX) + chr(0x31 + 0) + chr(self.brightness)
                + line.encode(ENCODING,'replace') + chr(LF))
        #self.log.debug(u'sending: ' + repr(cmd))
        if self.displayport:
            self.displayport.write(cmd)

    def show(self):
        self.window.show()

    def hide(self):
        self.window.show()

    def start(self):
        """Start threads."""
        if not self.started:
            self.ap.start()
            self.started = True

    def shutdown(self):
        """Cleanly shutdown."""
        if self.displayport is not None:
            self.displayport.close()
        if self.triggerport is not None:
            self.triggerport.close()
        self.ap.exit()
        self.ap.join()
        self.started = False

    def window_destroy_cb(self, window):
        """Handle destroy signal."""
        if self.started:
            self.shutdown()
        self.running = False
        gtk.main_quit()
    
    def area_expose_event_cb(self, widget, event):
        """Update desired portion of drawing area."""
        x , y, width, height = event.area
        widget.window.draw_drawable(widget.get_style().fg_gc[gtk.STATE_NORMAL],
                                    self.area_src, x, y, x, y, width, height)
        return False

    def area_redraw(self):
        """Lazy full area redraw method."""
        cr = self.area_src.cairo_create()
        pr = pangocairo.CairoContext(cr)
        cr.identity_matrix()

        # bg filled
        cr.set_source_rgb(0.85,0.85,0.90)
        cr.paint()

        # countdown box
        cbh = 0.56*self.height
        cbw = 0.98*self.width
        cbxo = 0.5 * (self.width-cbw)
        cbho = 0.5 * (self.height-cbh)
        cr.rectangle(cbxo, cbho, cbw, cbh)
        cr.set_source_rgb(0.92, 0.92, 1.0)
        cr.fill()

        cr.set_source_rgb(0.1, 0.1, 0.1)
        # time string txt
        if self.tod is not None:
            oh = 0.00 * self.height
            ch = 0.12 * self.height
            text_cent(cr, pr, oh, 0.5 * self.width,
                      self.tod.meridian(),
                      ch, TIMEFONT)

        # countdown txt
        if self.countdown is not None:
            ctx = u''
            if self.countdown >= 0:
                ctx = unicode(self.countdown)
            else:
                ctx = u'+' + unicode(-self.countdown)
            oh = 0.09 * self.height
            ch = 0.48 * self.height
            text_cent(cr, pr, oh, 0.5 * self.width, ctx, ch, COUNTERFONT)

        # rider name txt
        if self.riderstr is not None:
            oh = 0.80 * self.height
            ch = 0.10 * self.height
            #text_cent(cr, pr, oh, 0.5 * self.width,
                      #self.riderstr, ch, COUNTERFONT)
            fit_cent(cr, pr, oh, self.width,
                      self.riderstr, ch, COUNTERFONT)

        # starter bulbs
        if self.bulb is not None:
            rad = 0.12 * self.height
            oh = 0.5 * self.height
            ow = 0
            if self.bulb == 'red':
                ow = 0.15 * self.width
                cr.set_source_rgb(1.0, 0.2, 0.2)
            elif self.bulb == 'green':
                ow = 0.85 * self.width
                cr.set_source_rgb(0.2, 1.0, 0.2)
            cr.move_to(ow, oh)
            cr.arc(ow, oh, rad, 0, 6.3)
            cr.fill()

    def area_configure_event_cb(self, widget, event):
        """Re-configure the drawing area and redraw the base image."""
        x, y, width, height = widget.get_allocation()
        ow = 0
        oh = 0
        if self.area_src is not None:
            ow, oh = self.area_src.get_size()
        if width > ow or height > oh:
            self.area_src = gtk.gdk.Pixmap(widget.window, width, height)
        self.width = width
        self.height = height
        self.area_redraw()
        self.area.queue_draw()
        return True

    def clear(self):
        """Clear all elements and dearm timer."""
        self.countdown = None
        self.riderstr = None
        self.bulb = None
        self.armed = False
        
    def loadconfig(self):
        """Load config from disk."""
        cr = jsonconfig.config({u'countdown':{
                                    u'display':None,
                                    u'trigger':None,
                                    u'brightness': 0x31,
                                    u'fullscreen':False,
                                    u'syncthresh':DEFAUDIOSYNCTHRESH
                                    }})
        cr.add_section(u'countdown')
        # check for config file
        cfile = metarace.default_file(u'countdown.json')
        # read in sysdefaults before checking for config file
        cr.merge(metarace.sysconf, u'countdown')

        try:
            self.log.info(u'Reading config from: ' +repr(cfile))
            with open(cfile, 'rb') as f:
                cr.read(f)
        except Exception as e:
            self.log.error(u'Reading config: ' + unicode(e))

        if strops.confopt_bool(cr.get(u'countdown', u'fullscreen')):
            self.window.fullscreen()

        self.display = cr.get(u'countdown', u'display')
        if self.display is not None:
            self.displayport = serial.Serial(self.display,
                                             HL975_BAUD, timeout=0.2)
        self.trigger = cr.get(u'countdown', u'trigger')
        if self.trigger is not None:
            self.triggerport = serial.Serial(self.trigger, HL975_BAUD)

        self.set_brightness(strops.confopt_posint(
                                   cr.get(u'countdown', u'brightness'),
                                   1))
        # audio sync thresh
        self.syncthresh = strops.confopt_posint(
                                   cr.get(u'countdown', u'syncthresh'),
                                   DEFAUDIOSYNCTHRESH)
        self.log.info(u'Sync threshold set to: {0:0.3f}s'.format(
                                            float(self.syncthresh)*1e-9))

    def set_brightness(self, val):
        """Update local brightness."""
        nv = 0x31
        try:
            nv = int(val)
            if nv > 0 and nv < 4:
                nv = 0x30 + nv  # specified as 1, 2, 3
        except:
            self.log.info('Ignored invalid brightness: ' + repr(val))
        if nv in BRIGHTVALS:
            self.brightness = nv
        else:
            self.brightness = 0x31

    def draw_and_update(self, data=None):
        """Redraw in main loop, not in timeout."""
        self.area_redraw()
        self.area.queue_draw()
        return False

    def delayed_cursor(self):
        """Remove the mouse cursor from the text area."""
        pixmap = gtk.gdk.Pixmap(None, 1, 1, 1)
        color = gtk.gdk.Color()
        cursor = gtk.gdk.Cursor(pixmap, pixmap, color, color, 0, 0)
        self.area.get_window().set_cursor(cursor)
        return False

    def check_play_pos(self, expect):
        """Check and handle audio desync error."""
        # TODO: check pos using stream interface
        return False
        #try:
            #curpos,postype = self.player.query_position(gst.FORMAT_TIME, None)
            #err = abs(expect - curpos)
            #if err > self.syncthresh:
                #self.log.error(u'Audio desync detected: ' + repr(err) + 
                                #u'@' + repr(curpos))
                #self.player.set_state(gst.STATE_NULL)
            #else:
                #self.log.debug(u'Audio in sync, error=' + repr(err))
        #except Exception as e:
            #self.log.error(u'Reading audio position: ' + repr(e))
        return False

    def timeout(self, data=None):
        """Handle timeout."""

        # 1: Terminate?
        if not self.running:
            return False

        # 2: Process?
        try:
            ntime = tod.tod(u'now')
            ntod = ntime.truncate(0)
            if ntime >= self.nc.truncate(1):
                self.tod = ntod
                self.nc += tod.ONE
                self.process_timeout()
            else:
                self.log.debug(u'Timeout called early: ' + ntime.rawtime())
                # no need to advance, desired timeout not yet reached
        except Exception as e:
            self.log.error(u'Timeout: ' + unicode(e))

        # 3: Re-Schedule
        tt = tod.tod(u'now')+tod.tod(u'0.01')
        while self.nc < tt:	# ensure interval is positive
            if tod.MAX - tt < tod.ONE:
                self.log.debug(u'Midnight rollover.')
                break
            self.log.debug(u'May have missed an interval, catching up.')
            self.nc += tod.ONE	# 0.01 allows for processing delay
        ival = int(1000.0 * float((self.nc - tod.tod(u'now')).timeval))
        glib.timeout_add(ival, self.timeout)

        # 4: Return False
        return False	# must return False

    def key_event(self, widget, event):
        """Trigger countdown."""
        if event.type == gtk.gdk.KEY_PRESS:
          key = gtk.gdk.keyval_name(event.keyval) or 'None'
          if key in ['s', 'S', '.']:
            if self.currider is not None:
                self.log.debug(u'Stop Countdown.')
                self.currider = None
                self.startpending = False
            else:
                self.log.debug(u'Queue Countdown.')
                self.startpending = True
        return False

    def process_timeout(self):
        """Process countdown, redraw display if required."""
        curoft = tod2key(self.tod)
        cdn = None

        if self.startpending:
            self.currider = curoft + 31
            self.startpending = False

        if self.currider is not None:
            cdn = self.currider - curoft
            if cdn > 30:
                cdn = 30
            if cdn == 10:
                self.ap.play()
                #self.player.set_state(gst.STATE_PLAYING)
                self.bulb = 'red'
            elif cdn in [8, 7, 6]:	# check audio stream sync
                self.check_play_pos(int((10-cdn)*1e9))
            elif cdn == 15:
                self.ap.stop()
                #self.player.set_state(gst.STATE_PAUSED)
                self.bulb = 'red'
            elif cdn == 30:
                self.bulb = 'red'
            elif cdn == 5:
                self.armed = True	# self arm is not same as timer arm
            elif cdn == 0:
                self.bulb = 'green'
                self.countdown = 0
                if self.triggerport is not None:
                    self.triggerport.setRTS(0)
                
            elif cdn == -1:
                self.clear() # note also removes the bulb
                self.currider = None
                cdn = 0	# hackit

            if cdn >= 0 and cdn <= 30:
                if self.bulb:
                    self.countdown = cdn
                else:
                    self.countdown = None
            else:
                self.countdown = None
        else:
            self.clear()	# also does dearm
            self.riderstr = u''
            # no more riders or error in init.
        self.setcdn(cdn)
        if self.triggerport is not None:
            self.triggerport.setRTS(1)
        self.draw_and_update()

    def gst_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)	# close player
        elif t == gst.MESSAGE_ERROR:
            self.player.set_state(gst.STATE_NULL)
            err, debug = message.parse_error()
            self.log.error(u"gst error: %s" % err, debug)
        else:
            pass
            #self.log.debug(u"gst message: " + repr(message))

    def __init__(self):
        # logger and handler
        self.log = logging.getLogger()
        self.log.setLevel(logging.DEBUG)
        self.loghandler = logging.FileHandler(LOGFILE)
        self.loghandler.setLevel(logging.DEBUG)
        self.loghandler.setFormatter(logging.Formatter(
                       '%(asctime)s %(levelname)s:%(name)s: %(message)s'))
        self.log.addHandler(self.loghandler)
        self.log.info(u'IRTT Starter - Init.')

        #self.scb = telegraph.telegraph()

        self.started = False
        self.running = True
        self.startpending = False
        self.display = None
        self.displayport = None
        self.trigger = None
        self.triggerport = None
        self.brightness = 0x31

        # Audio output
        self.player = gst.element_factory_make("playbin2", "player")
        self.player.set_property("audio-sink",
                         gst.element_factory_make("alsasink", "sink"))
        self.player.set_property("video-sink",
                         gst.element_factory_make("fakesink", "fakesink"))
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.gst_message)
        self.player.set_property('uri', u'file://'
                             + os.path.join(metarace.DB_PATH, u'start.wav'))

        # variables
        self.armed = False
        self.width = 0
        self.height = 0
        self.syncthresh = 100000000
        self.tod = tod.tod(u'now').truncate(0)
        self.nc = self.tod + tod.tod(u'1.22') # set interval a little off mark
        self.countdown = None
        self.riderstr = None
        self.bulb = None
        self.currider = None
        self.window = gtk.Window()
        self.window.set_title(u'Start Clock')
        self.window.connect('destroy', self.window_destroy_cb)
        self.area_src = None
        self.area = gtk.DrawingArea()
        self.area.connect('configure_event', self.area_configure_event_cb)
        self.area.connect('expose_event', self.area_expose_event_cb)
        self.area.set_size_request(400,220)
        self.area.show()
        self.window.add(self.area)
        self.window.connect('key-press-event', self.key_event)
        self.log.info(u'Starting clock intervals at: ' + self.nc.rawtime(3))
        glib.timeout_add(2000, self.timeout)
        glib.timeout_add_seconds(5, self.delayed_cursor)

def main():
    """Run the application."""
    configpath = None
    # expand config on cmd line to realpath _before_ doing chdir
    if len(sys.argv) > 2:
        print(u'usage: countdown [configdir]\n')
        sys.exit(1)
    elif len(sys.argv) == 2:
        configpath = os.path.realpath(os.path.dirname(sys.argv[1]))

    metarace.init()
    if configpath is not None:
        os.chdir(configpath)
    app = countdown()
    app.loadconfig()
    app.show()
    app.start()
    try:
        metarace.mainloop()
    except:
        app.shutdown()
        raise

if __name__ == '__main__':
    main()

