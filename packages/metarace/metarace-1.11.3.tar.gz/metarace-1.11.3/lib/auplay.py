
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

"""Pygame audio player"""

import logging
import threading
import pygame

class auplay(threading.Thread):
    """Audio player object class."""
    def __init__(self, filename=u'start.wav', name=u'auplay'):
        threading.Thread.__init__(self) 
        self.running = False
        self.s = None
        self.name = name
        self.filename = filename
        self.log = logging.getLogger(self.name)
        self.log.setLevel(logging.DEBUG)

    def setfile(self, filename=None):
        self.filename = filename
        if self.running:
            self.s = pygame.mixer.Sound(self.filename)

    def play(self):
        """Start playback."""
        if self.s is not None:
            self.s.play()

    def stop(self):
        """Stop playback."""
        if self.s is not None:
            self.s.stop()

    def exit(self, msg=None):
        """Request thread termination."""
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    def run(self):
        self.log.debug(u'Starting')

        pygame.init()
        pygame.mixer.init()
        self.running = True
        self.s = pygame.mixer.Sound(self.filename)    

        while self.running:
            try:
                ev = pygame.event.wait()
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    self.running = False
            except Exception as e:
                self.log.error('Exception: ' + str(type(e)) + str(e))
        self.log.info('Exiting')

if __name__ == "__main__":
    import metarace
    import time
    ap = auplay(metarace.default_file('start.wav'))
    ap.start()
    # first run will not sound because s is not yet ready
    try:
        count = 0
        while count < 5:
            ap.play()
            time.sleep(9.0)
            ap.stop()
            time.sleep(1.0)
            count += 1
    except: 
        pass
    ap.exit('End')
    ap.join()
