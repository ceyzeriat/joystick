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
          * Create a custom method decorated with :py:data:`~joystick.deco.deco_before` or
           :py:data:`~joystick.deco.deco_after` to add to the initialization of the frame.

        Kwargs:
          * Will be passed to the optional custom methods

        Raises:
          N/A
        """
        before, after = core.extract_callit(self, 'init')
        core.callmthd(self, before, **kwargs)
        self._dead = False
        self._frames = []
        self._running = False
        # core.INITMETHOD left for backward compatibility
        core.callmthd(self, after + [core.INITMETHOD], **kwargs)

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
        if value:
            self.start()
        else:
            self.stop()

    def _push_status_to_all_frames(self):
        """
        Push running status to all frames
        """
        for item in self._frames:
            item._mummy_running = self._running


    def add_frame(self, frame, **kwargs):
        """
        Adds a frame to the simulation. Use it as:

        >>> self.mygraph = self.add_frame(frame)
        """
        before, after = core.extract_callit(self, 'add_frame')
        core.callmthd(self, before, **kwargs)
        self._frames.append(frame)
        core.callmthd(self, after, **kwargs)
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

    def start(self, **kwargs):
        """
        Starts the simulation if not already running nor exited
        Starts each individual frame (calls `~joystick.Joystick.start_frames`)
        """
        if self._dead or self._running:
            return
        self._running = True
        before, after = core.extract_callit(self, 'start')
        core.callmthd(self, before + self._get_infinite_loop_fcts(), **kwargs)
        self._push_status_to_all_frames()
        self.start_frames()
        core.callmthd(self, after, **kwargs)

    def start_frames(self):
        """
        Turns on the updating of all frames, keeps the simulation
        as it was, running or not
        """
        for item in self._frames:
            item.start()

    def stop(self, **kwargs):
        """
        Stops the simulation if not exited nor already stopped
        Does not individually stop each frames, although frames will
        stop updating given that the simulation is no longer running;
        i.e. does not call `~joystick.Joystick.start_frames`.
        """
        if self._dead or not self._running:
            return
        self._running = False
        before, after = core.extract_callit(self, 'stop')
        core.callmthd(self, before, **kwargs)
        self._push_status_to_all_frames()
        core.callmthd(self, after, **kwargs)

    def stop_frames(self):
        """
        Stops all frames from updating, the simulation continues
        running
        """
        for item in self._frames:
            item.stop()

    def exit(self, **kwargs):
        """
        Terminates the simulation
        """
        before, after = core.extract_callit(self, 'exit')
        core.callmthd(self, before, **kwargs)
        for item in self._frames:
            if item.visible:
                item.exit()
        self.stop()
        self._dead = True
        time.sleep(0.2)
        core.callmthd(self, after, **kwargs)
