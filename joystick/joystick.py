#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#  
#  JOYSTICK - Real-time plotting and logging while console controlling
#  Copyright (C) 2016  Guillaume Schworer
#  
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#  
#  For any information, bug report, idea, donation, hug, beer, please contact
#    guillaume.schworer@gmail.com
#
###############################################################################

from . import core
np = core.np
time = core.time


__all__ = ['Joystick']


class Joystick(object):
    def __init__(self, **kwargs):
        """
        Main class to be wrapped (see ./joystick/example.py)

        [Optional]
          * Create a custom method ``core.INITMETHOD`` to add to the initialization of
            the class.

        Kwargs:
          * Will be passed to the optional custom methods

        Raises:
          N/A
        """
        self._dead = False
        self._frames = []
        self._running = False
        core.callit(self, core.INITMETHOD, **kwargs)

    @property
    def running(self):
        """
        Returns ``True`` if the simulation is running
        Set to ``True``/``False`` to start/stop the simulation
        """
        return self._running
    
    @running.setter
    def running(self, value):
        if self._dead:
            return
        self._running = bool(value)
        for item in self._frames:
            item._mummy_running = self._running
        if self._running:
            for item in self._get_infinite_loop_fcts():
                core.callit(self, item)
            for item in self._frames:
                if item.visible:
                    item.start()

    def add_frame(self, frame):
        """
        Adds a frame to the simulation. Use it as:

        >>> self.mygraph = self.add_frame(frame)
        """
        self._frames.append(frame)
        return frame

    @classmethod
    def _get_infinite_loop_fcts(self):
        """
        Returns a list of all functions decorated with the 
        infinite_loop decorator
        """
        if hasattr(self, '_infinite_loop'):
            return self._infinite_loop.fcts
        return []

    def start(self):
        """
        Starts the simulation
        """
        self.running = True

    def start_frames(self):
        """
        Turns on the updating of all frames, keeps the simulation
        as it was, running or not
        """
        for item in self._frames:
            item.start()

    def stop(self):
        """
        Stops the simulation and all frames
        """
        self.running = False

    def stop_frames(self):
        """
        Stops all frames from updating, the simulation continues
        running
        """
        for item in self._frames:
            item.stop()

    def exit(self):
        """
        Terminates the simulation
        """
        for item in self._frames:
            if item.visible:
                item.exit()
        self.stop()
        self._dead = True
        time.sleep(0.2)
