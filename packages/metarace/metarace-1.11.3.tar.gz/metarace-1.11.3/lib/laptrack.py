
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

"""Lap tracker console"""

import pygtk
pygtk.require("2.0")

import gtk
import glib
import pango
import pangocairo
import logging
import os
import sys

import metarace
from metarace import tod
from metarace import timy
from metarace import telegraph
from metarace import strops
from metarace import ucsv
from metarace import jsonconfig

# Global Defaults
USCBSRV_CHANNEL=u'#agora'
#USCBSRV_CHANNEL=u'#announce'

# Globals
CONFIGFILE=u'laptrack.json'
LOGFILE=u'laptrack.log'
TIMEFONT='Nimbus Sans L Condensed Bold '
COUNTERFONT='Nimbus Sans L Condensed Bold '
NOHDR = [u'Start', u'start', u'time', u'Time', u'']
# TYPICAL SYNC ERROR: 17619048	# typical playback error ~20ms
#DEFAUDIOSYNCTHRESH = 100000000	# Tolerate no more than 100ms audio desync
				# note: on Pi/ARM, 200ms reqd due to proc lag
                                # this is now configurable
				# TODO: not currently used

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

class laptrack(object):
    """LAp track Display application."""
 
    def show(self):
        self.window.show()

    def hide(self):
        self.window.show()

    def start(self):
        """Start threads."""
        if not self.started:
            self.scb.start()
            self.started = True

    def shutdown(self):
        """Cleanly shutdown."""
        self.scb.exit()
        self.scb.join()
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
        cr.set_source_rgb(0.92,0.92,1.0)
        cr.paint()

        cr.set_source_rgb(0.1, 0.1, 0.1)
        # info txt
        if self.infotxt is not None:
            oh = 0.06 * self.height
            ch = 0.35 * self.width
            text_cent(cr, pr, oh, 0.5 * self.width, self.infotxt, ch, COUNTERFONT)

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
        pass
        
    def loadconfig(self):
        """Load config from disk."""
        cr = jsonconfig.config({u'laptrack':{
                                    u'uscbsrv':'',
                                    u'channel':USCBSRV_CHANNEL, 
                                    u'fullscreen':False,
                                    u'backlightlow':0.25,
                                    u'backlighthigh':1.0,
                                    u'backlightdev':None,
                                    u'datakey':u'laptime'}})
        cr.add_section(u'laptrack')
        # check for config file
        cfile = metarace.default_file(CONFIGFILE)
        # read in sysdefaults before checking for config file
        cr.merge(metarace.sysconf, u'laptrack')

        try:
            self.log.info(u'Reading config from: ' +repr(cfile))
            with open(cfile, 'rb') as f:
                cr.read(f)
        except Exception as e:
            self.log.error(u'Reading config: ' + unicode(e))

        if strops.confopt_bool(cr.get(u'laptrack', u'fullscreen')):
            self.dofullscreen = True

        # load backlight parameters
        self.backlightdev = cr.get(u'laptrack', u'backlightdev')
        self.backlightlow = strops.confopt_float(cr.get(u'laptrack',
                                                 u'backlightlow'),0.25)
        self.backlighthigh = strops.confopt_float(cr.get(u'laptrack',
                                                 u'backlighthigh'),1.0)
        if self.backlightdev is not None and os.path.exists(self.backlightdev):
            try:
                with open(os.path.join(self.backlightdev,u'max_brightness'),
                                       'rb') as bf:
                    mbstr = bf.read()
                    self.backlightmax = strops.confopt_posint(mbstr,20)
                    self.backlightdev = os.path.join(self.backlightdev,
                                                     u'brightness')
                    self.log.info(u'Using backlight dev '
                                    + repr(self.backlightdev) 
                                    + u'; Max={0}, Low={1}%, High={2}%'.format(
                                        self.backlightmax,
                                        int(100.0*self.backlightlow),
                                        int(100.0*self.backlighthigh)))
            except Exception as e:
                self.log.error(u'Reading from backlight device: ' + repr(e))
                self.backlightdev = None
        else:
            self.log.info(u'Backlight control not configured.')
            self.backlightdev = None

        # set sender port
        nhost = cr.get(u'laptrack', u'uscbsrv')
        nchannel = cr.get(u'laptrack', u'channel')
        self.scb.set_portstr(nhost, nchannel)

        # set data key value
        self.datakey = cr.get(u'laptrack', u'datakey')

    def draw_and_update(self, data=None):
        """Redraw in main loop, not in timeout."""
        self.area_redraw()
        self.area.queue_draw()
        return False

    def delayed_cursor(self):
        """Remove the mouse cursor from the text area."""
        if self.dofullscreen:
            self.window.fullscreen()
        pixmap = gtk.gdk.Pixmap(None, 1, 1, 1)
        color = gtk.gdk.Color()
        cursor = gtk.gdk.Cursor(pixmap, pixmap, color, color, 0, 0)
        self.area.get_window().set_cursor(cursor)
        return False

    def remote_msg(self, msg):
        """Log a message to the uscbsrv."""
        pass
        #self.log.debug(msg)
        #self.scb.add_rider([msg], u'message')

    def timeout(self, data=None):
        """Handle timeout."""
        return False

    def set_backlight(self, percent=None):
        """Attempt to adjust screen brightness between riders."""
        if self.backlightdev and abs(percent - self.backlight) > 0.05:
            if percent < 0.0:
                percent = 0.0
            elif percent > 1.0:
                percent = 1.0
            nb = int(0.5 + percent * self.backlightmax)
            try:
                with open(self.backlightdev, 'wb') as f:
                    f.write(str(nb))
            except Exception as e:
                self.log.error(u'Writing to backlight control: ' + repr(e))
            self.backlight = percent

    def process_timeout(self):
        """Process countdown, redraw display if required."""
        self.draw_and_update()

    def remote_cb(self, cmd, nick, chan):
        """Handle unt message from remote (in main loop)."""
        if cmd.header == self.datakey:
            self.infotxt = cmd.text
            self.draw_and_update()

    def __init__(self):
        # logger and handler
        self.log = logging.getLogger()
        self.log.setLevel(logging.DEBUG)
        self.loghandler = logging.FileHandler(LOGFILE)
        self.loghandler.setLevel(logging.DEBUG)
        self.loghandler.setFormatter(logging.Formatter(
                       '%(asctime)s %(levelname)s:%(name)s: %(message)s'))
        self.log.addHandler(self.loghandler)
        self.log.info(u'Lap Track - Init')

        # require only telegraph
        self.scb = telegraph.telegraph()
        self.scb.set_pub_cb(self.remote_cb)

        self.started = False
        self.running = True

        # variables
        self.infotxt = None
        self.width = 0
        self.height = 0
        self.backlight = 0.0
        self.backlightmax = 20
        self.backlightdev = None
        self.backlightlow = 0.25
        self.backlighthigh = 1.0
        self.dofullscreen = False
        self.window = gtk.Window()
        self.window.set_title(u'Lap Track')
        self.window.connect('destroy', self.window_destroy_cb)
        self.area_src = None
        self.area = gtk.DrawingArea()
        self.area.connect('configure_event', self.area_configure_event_cb)
        self.area.connect('expose_event', self.area_expose_event_cb)
        self.area.set_size_request(640,480)
        self.area.show()
        self.window.add(self.area)
        #glib.timeout_add(2000, self.timeout)
        glib.timeout_add_seconds(5, self.delayed_cursor)

def main():
    """Run the application."""
    configpath = None
    # expand config on cmd line to realpath _before_ doing chdir
    if len(sys.argv) > 2:
        print(u'usage: laptrack [configdir]\n')
        sys.exit(1)
    elif len(sys.argv) == 2:
        configpath = os.path.realpath(os.path.dirname(sys.argv[1]))

    metarace.init()
    if configpath is not None:
        os.chdir(configpath)
    app = laptrack()
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

