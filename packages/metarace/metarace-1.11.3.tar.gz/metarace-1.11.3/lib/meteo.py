
# Metarace : Cycle Race Abstractions
# Copyright (C) 2012-15  Nathan Fraser
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

"""Yocto-Meteo Interface."""

# Yocto device is polled in a separate thread, on error all values
# are invalidated. Check status with connected():
#
# if m.connected():
#   temp = m.t
# 

import threading
import logging
import time	# for sleep in main thread
import usb.core

# Meteo 'start' command
scmd = bytearray(64)
scmd[1] = 0xf9
scmd[2] = 0x09
scmd[3] = 0x02
scmd[4] = 0x01

# Meteo 'config' command
ccmd = bytearray(64)
ccmd[0] = 0x08
ccmd[1] = 0xf9
ccmd[2] = 0x01

TIMEOUT = 1000	# libusb call timeout

class meteo(threading.Thread):
    """Yocto-Meteo Object"""
    def __init__(self):
        threading.Thread.__init__(self) 
        self.__m = None
        self.t = 0.0
        self.h = 0.0
        self.p = 0.0
        self.__stat = False
        self.__running = False
        self.log = logging.getLogger(u'meteo')
        self.log.setLevel(logging.DEBUG)

    def connected(self):
        return self.__stat

    def envstr(self):
        """Return a formatted environment string."""
        ret = u'n/a'
        if self.connected():
            ret = u'{0:0.1f},{1:0.0f},{2:0.0f}'.format(
                    self.t, self.h, self.p)
        return ret

    def exit(self):
        """Request thread termination."""
        self.__running = False

    def __connect(self):
        """Request re-connect, exceptions should bubble up to run loop."""
        self.log.debug('Re-connect meteo')
        self.__cleanup()
        self.__stat = False	# superfluous
        self.__m = usb.core.find(idVendor=0x24e0, idProduct=0x0018)
        if self.__m is not None:
            if self.__m.is_kernel_driver_active(0):
                self.log.debug('Detach kernel driver')
                self.__m.detach_kernel_driver(0)
            self.__m.reset()
            # clear any junk in the read buffer - so that init cmds will send
            try:
                while True:
                    junk = self.__m.read(0x81, 64, 50)
            except usb.core.USBTimeoutError:
                pass
            # send start and conf commands errors here are collected in run
            self.__m.write(0x01, scmd)
            self.__m.write(0x01, ccmd)
            self.__stat = True

    def __cleanup(self):
        self.log.debug('Close and cleanup connection')
        if self.__m is not None:
            try:
                usb.util.dispose_resources(self.__m)
            except:
                self.log.warn('Error disposing resources - possible leak');
                pass
        self.__m = None
        self.__stat = False
        time.sleep(0.1)	# release thread

    def __read(self):
        bd = bytearray(self.__m.read(0x81, 64))
        of = 0
        while of < 64:
            pktno = bd[of]&0x7;
            stream = (bd[of]>>3)&0x1f;
            pkt = bd[of+1]&0x3;
            size = (bd[of+1]>>2)&0x3f;
            if stream == 3 and size > 0:
                sb = bd[of+2]
                if sb in [0x01, 0x02, 0x03]:
                    val = float(bd[of+3:of+3+size-1].decode('ascii','ignore'))
                    if sb == 1:
                        self.t = val
                    elif sb == 2:
                        self.p = val
                    elif sb == 3:
                        self.h = val
            of += size+2

    def run(self):
        """Called via threading.Thread.start()."""
        self.__running = True
        self.log.debug('Starting')
        while self.__running:
            try:
                if self.__stat and self.__m is not None:
                    try:
                        self.__read()
                    except usb.core.USBTimeoutError:
                        pass
                else:
                    self.__connect()
                    self.log.debug(u'Meteo re-connect: ' + repr(self.__m))
                    time.sleep(5.0)
            except Exception as e:
                self.log.error('Exception: ' + str(type(e)) + str(e))
                self.__stat = False
                time.sleep(1.0)
        self.__cleanup()
        self.log.info('Exiting')

def printval(h=None):
    print(h.envstr())
    return True

if __name__ == "__main__":
    import metarace
    import gtk
    import glib
    import time
    metarace.init()
    y = meteo()
    lh = logging.StreamHandler()
    lh.setLevel(logging.DEBUG)
    y.log.addHandler(lh)
    try:
        y.start()
        glib.timeout_add_seconds(15, printval, y)	# in main loop?
        metarace.mainloop()
    except:
        y.exit()
        y.join()
        raise
