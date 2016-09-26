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
Tkinter = core.Tkinter
np = core.np


__all__ = ['Frame']


class Frame(object):
    def __init__(self, daddy, name, freq_up, pos=(50, 50), size=(400, 400),
                 screen_relative=False, **kwargs):
        """
        Initialization
        """
        # save input for reinit
        kwargs['daddy'] = daddy
        kwargs['name'] = name
        kwargs['freq_up'] = freq_up
        kwargs['pos'] = pos
        kwargs['size'] = size
        kwargs['screen_relative'] = screen_relative
        self._kwargs = kwargs
        # list this frame
        daddy._frames.append(self)
        # main simu not running
        self._mummy_running = False
        self._init_frame(**self._kwargs)

    def _init_frame(self, **kwargs):
        self.freq_up = float(kwargs.pop('freq_up'))
        self._running = True and not self._mummy_running
        self._visible = True
        self._window = Tkinter.Tk()
        self._window.title(str(kwargs.pop('name')))
        self._window.protocol("WM_DELETE_WINDOW", self.exit)
        pos = tuple(kwargs.pop('pos')[:2])
        size = tuple(kwargs.pop('size')[:2])
        if bool(kwargs.pop('screen_relative')):
            w = self._window.winfo_screenwidth()
            h = self._window.winfo_screenheight()
            pos = np.round(np.array(pos) * (w, h)).astype(int)
            size = np.round(np.array(size) * (w, h)).astype(int)
        self._window.geometry("{}x{}+{}+{}".format(*(size + pos)))

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        print("{}Reserved attribute, use 'exit' or 'reinit' methods.{}" \
            .format(core.font.red, core.font.normal))

    @property
    def typ(self):
        return "_{}".format(self.__class__.__name__.lower())

    @typ.setter
    def typ(self, value):
        print("{}Read-only.{}".format(core.font.red, core.font.normal))
    
    def reinit(self, **kwargs):
        """
        Re-init, closes old and creates new, input params are
        that of the constructor.
        'None' is reuse the previous parameters
        """
        try:
            self.exit()
        except Tkinter.TclError:  # already closed
            pass
        # updates with new reinit value if specified
        self._kwargs.update(kwargs)
        self._init_frame(**self._kwargs)

    @property
    def running(self):
        return self._running
    
    @running.setter
    def running(self, value):
        if value:
            self.start()
        else:
            self.stop()

    @property
    def freq_up(self):
        return self._freq_up

    @freq_up.setter
    def freq_up(self, value):
        self._freq_up = np.clip(value, 1e-3, 1e3)

    def _update_loop(self):
        """
        Does the calling-loop job
        """
        if self._mummy_running and self.running:
            core.callit(self, core.PREUPDATEMETHOD)
            core.callit(self, core.UPDATEMETHOD)
            self.show()
            self._window.after(int(1000./self.freq_up), self._update_loop)

    def start(self):
        """
        Starts updating the frame
        """
        self._running = True
        self._update_loop()

    def stop(self):
        """
        Stops updating the frame
        """
        self._running = False

    def exit(self):
        """
        Terminates the frame
        """
        self.stop()
        if self.visible:
            self._window.destroy()
        self._visible = False
