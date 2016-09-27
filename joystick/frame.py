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
tkinter = core.tkinter
np = core.np


__all__ = ['Frame']


class Frame(object):
    def __init__(self, name, freq_up, pos=(50, 50), size=(400, 400),
                 screen_relative=False, **kwargs):
        """
        Initialises a frame, a base-class used to contain a e.g.
        :py:class:`Graph` or :py:class:`Text`.

        [Optional]
          * Create a custom method ``core.INITMETHOD`` to add to the
            initialization of the frame.
          * Create a custom method ``core.UPDATEMETHOD`` to add code at
            the updating of the frame.

        Args:
          * name (str): the frame name
          * freq_up (float or None): the frequency of update of the
            frame, between 1e-3 and 1e3 Hz, or ``None`` for no update
          * pos (px or %) [optional]: left-top corner position of the
            frame, see ``screen_relative``
          * size (px or %) [optional]: width-height dimension of the
            frame, see ``screen_relative``
          * screen_relative (bool) [optional]: set to ``True`` to give
            ``pos`` and ``size`` as a % of the screen size, or ``False``
            to give then as pixels

        Kwargs:
          * Will be passed to the optional custom methods
        """
        # save input for reinit
        kwargs['name'] = name
        kwargs['freq_up'] = freq_up
        kwargs['pos'] = pos
        kwargs['size'] = size
        kwargs['screen_relative'] = screen_relative
        self._kwargs = kwargs
        # main simu not running
        self._mummy_running = False
        self._init_frame(**self._kwargs)

    def _init_frame(self, **kwargs):
        """
        Separate function from __init__ for re-initialization purpose
        """
        self.freq_up = float(kwargs.pop('freq_up'))
        self._running = True and not self._mummy_running
        self._visible = True
        self._window = tkinter.Tk()
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
        core.callit(self, core.INITMETHOD, **kwargs)

    @property
    def visible(self):
        """
        Returns ``True`` if the frame has not been closed. Read-only.
        """
        return self._visible

    @visible.setter
    def visible(self, value):
        raise Exception('hoho')
        #print("{}Reserved attribute, use 'exit' or 'reinit' methods.{}" \
        #    .format(core.font.red, core.font.normal))

    @property
    def typ(self):
        """
        Returns the type of the frame, e.g. ``Graph``. Read-only.
        """
        return "_{}".format(self.__class__.__name__.lower())

    @typ.setter
    def typ(self, value):
        print("{}Read-only.{}".format(core.font.red, core.font.normal))
    
    def reinit(self, **kwargs):
        """
        Re-initializes the frame, i.e. closes the current frame if
        necessary and creates a new one. Uses the parameters of
        initialization by default or anything provided through kwargs.
        See class :py:class:`Frame` for the description of input parameters.
        """
        try:
            self.exit()
        except tkinter.TclError:  # already closed
            pass
        # updates with new reinit value if specified
        self._kwargs.update(kwargs)
        self._init_frame(**self._kwargs)

    @property
    def running(self):
        """
        Returns ``True`` if the frame should update
        Set to ``True``/``False`` to start/stop the updating
        """
        return self._running
    
    @running.setter
    def running(self, value):
        if value:
            self._running = True
            self._update_loop()
        else:
            self._running = False

    @property
    def freq_up(self):
        """
        Update frequency (Hz) of the frame.
        Set between 1e-3 and 1e3 Hz, or ``None`` for no updating
        """
        return self._freq_up

    @freq_up.setter
    def freq_up(self, value):
        if value in [None, False]:
            self._freq_up = None
        else:
            self._freq_up = np.clip(value, 1e-3, 1e3)

    def _update_loop(self):
        """
        Performs the loop-calling job
        """
        if self._mummy_running and self.running and self._freq_up is not None:
            core.callit(self, core.PREUPDATEMETHOD)
            core.callit(self, core.UPDATEMETHOD)
            self.show()
            self._window.after(int(1000./self.freq_up), self._update_loop)

    def start(self):
        """
        Starts updating the frame
        """
        self.running = True

    def stop(self):
        """
        Stops updating the frame
        """
        self.running = False

    def exit(self):
        """
        Terminates the frame
        """
        self.stop()
        if self.visible:
            self._window.destroy()
        self._visible = False
