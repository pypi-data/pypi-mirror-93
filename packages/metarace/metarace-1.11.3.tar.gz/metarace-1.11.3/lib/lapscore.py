
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

"""Lap score app for DISC

"""

LOGFILE = 'lapscore.log'

import pygtk
pygtk.require("2.0")

import gtk
import glib
import pango
import logging
import os
import sys

import metarace
from metarace import gemini

class lapscore(object):
 
    def show(self):
        self.window.show()

    def hide(self):
        self.window.hide()

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

    def clear(self):
        """Force clear."""
        self.lap = None
        self.entry.set_text('')
        self.scb.clear()

    def cancel(self):
        """Cancel manual override."""
        if self.lap is not None:
            self.entry.set_text(self.lap)
        self.lap = None

    def entry_activate(self, entry, data=None):
        """Set lap and re-send."""
        self.lap = None
        self.scb.set_lap(self.entry.get_text())
        
    def increment(self, step=1):
        """Try and increment current value."""
        self.lap = None
        cstr = self.entry.get_text()
        if cstr.isdigit():
            cval = int(cstr) + step
            if cval < 0:
                cval = 0
            elif cval > 999:
                cval = 999
            cstr = str(cval)
        self.entry.set_text(cstr)
        self.scb.set_lap(cstr)

    # ck 23/07
    def key_event(self, widget, event):
        """Collect key events on main window."""
        if event.type == gtk.gdk.KEY_PRESS:
            key = gtk.gdk.keyval_name(event.keyval) or 'None'
            if event.state & gtk.gdk.CONTROL_MASK:
                key = key.lower()
                if key == 'q':
                    self.window.destroy()
                    return True
            else:
                if len(key) == 1:	# lazy 'one' char key
                    if self.lap is None:
                        self.lap = self.entry.get_text()
                        self.entry.set_text('')
                elif key == 'Escape':
                    if self.lap is not None:
                        self.cancel()
                        return True
                elif key == 'Up':
                    self.increment(1)
                    return True
                elif key == 'Page_Up':
                    self.increment(10)
                    return True
                elif key == 'Down':
                    self.increment(-1)
                    return True
                elif key == 'Page_Down':
                    self.increment(-10)
                    return True
                elif key == 'Delete':
                    self.clear()
                    return True
                # return true if key handled
        return False

    def __init__(self):
        # logger and handler
        self.log = logging.getLogger()
        self.log.setLevel(logging.DEBUG)
        self.loghandler = logging.FileHandler(LOGFILE)
        self.loghandler.setLevel(logging.DEBUG)
        self.loghandler.setFormatter(logging.Formatter(
                       '%(asctime)s %(levelname)s:%(name)s: %(message)s'))
        self.log.addHandler(self.loghandler)
        self.log.debug('Lapscore - Init.')

        # status
        self.lap = None

        # one gemini sender
        self.scb = gemini.gemini()

        self.started = False
        self.running = True

        self.window = gtk.Window()
        self.window.set_title('DISC Lap Score')
        self.window.connect('destroy', self.window_destroy_cb)
        self.window.connect('key-press-event', self.key_event)
        self.entry = gtk.Entry(3)
        self.entry.set_width_chars(4)
        self.entry.show()
        self.entry.modify_font(pango.FontDescription('Nimbus Sans L Condensed Bold 120'))
        self.entry.connect('activate', self.entry_activate)
        self.window.add(self.entry)

def main():
    """Run the application."""
    if len(sys.argv) == 2:
        port = sys.argv[1]
    else:
        port = '/dev/ttyUSB0'
    metarace.init()
    app = lapscore()
    app.show()
    app.scb.setport(port)
    app.start()
    try:
        metarace.mainloop()
    except:
        app.shutdown()
        raise

if __name__ == '__main__':
    main()

