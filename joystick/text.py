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
time = core.time
from .frame import Frame


__all__ = ['Text']


class Text(Frame):
    def __init__(self, name, freq_up=1, pos=(50, 50), size=(400, 400),
                 screen_relative=False, background="black",
                 foreground='green', rev=True, font=("consolas", 11),
                 mark_line=True, mark_fmt='%H:%M:%S > ', scrollbar=True,
                 **kwargs):
        """
        Initialises a text-frame. Use :py:func:`~joystick.text.Text.add_text` to add text to it.

        [Optional]
          * Create a custom method :py:data:`~joystick.core.INITMETHOD` to add to the
            initialization of the frame.
          * Create a custom method :py:data:`~joystick.core.UPDATEMETHOD` to add code at
            the updating of the frame.

        Args:
          * name (str): the frame name
          * freq_up (float or None): the frequency of update of the frame,
            between 1e-3 and 1e3 Hz, or ``None`` for no update
          * pos (px or %) [optional]: left-top corner position of the
            frame, see ``screen_relative``
          * size (px or %) [optional]: width-height dimension of the
            frame, see ``screen_relative``
          * screen_relative (bool) [optional]: set to ``True`` to give
            ``pos`` and ``size`` as a % of the screen size, or ``False``
            to give then as pixels
          * background (color) [optional]: background color of the frame
          * foreground (color) [optional]: text color of the frame
          * rev (bool) [optional]: if ``True``, a new line will be added on
            the top of the text
          * font (tuple (font, size)) [optional]: the font of the text
          * mark_line (bool) [optional]: if ``True``, each line will be
            prepended using the ``Text.mark_fmt`` format
          * mark_fmt (str) [optional]: ``time.strftime`` format to be used
            for (optionally) prepending each text added to the frame
          * scrollbar (bool) [optional]: if ``True``, a Y-scrollbar is added

        Kwargs:
          * wrap (str): wrap mechanism (default 'word')
          * undo (bool): authorized undoing if ``True``
          * Any parameters accepted by ``tkinter.Text`` (non-abbreviated)
          * Will be passed to the optional custom methods
        """
        # save input for reinit
        kwargs['name'] = name
        kwargs['freq_up'] = freq_up
        kwargs['pos'] = pos
        kwargs['size'] = size
        kwargs['screen_relative'] = screen_relative
        kwargs['background'] = background
        kwargs['foreground'] = foreground
        kwargs['rev'] = rev
        kwargs['font'] = font
        kwargs['mark_line'] = mark_line
        kwargs['mark_fmt'] = mark_fmt
        kwargs['scrollbar'] = scrollbar
        self._kwargs = kwargs
        # call mummy init
        super(Text, self).__init__(**self._kwargs)
        # call ya own init
        self._init_base(**self._kwargs)

    def _init_base(self, **kwargs):
        """
        Separate function from __init__ for re-initialization purpose
        """
        self._lines_to_insert = []
        self._isempty = True
        self.rev = bool(kwargs.pop('rev'))
        self.mark_line = bool(kwargs.pop('mark_line'))
        self.mark_fmt = kwargs.pop('mark_fmt')
        self._text = tkinter.Text(master=self._window, **core.tkkwargs(kwargs))
        self._text.config(font=kwargs.pop('font'),
                          undo=kwargs.pop('undo', True),
                          wrap=kwargs.pop('wrap', 'word'))
        if kwargs.pop('scrollbar'):
            scrollbar = tkinter.Scrollbar(self._text)
            scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
            self._text.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=self._text.yview)
        self._text.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)            
        # call the user's init if existing
        core.callit(self, core.PREUPDATEMETHOD)
        core.callit(self, core.INITMETHOD, **kwargs)

    def reinit(self, **kwargs):
        """
        Re-initializes the frame, i.e. closes the current frame if
        necessary and creates a new one. Uses the parameters of
        initialization by default or anything provided through kwargs.
        See class :py:class:`~joystick.text.Text` for the description of input parameters.
        """
        # updates with new reinit value if specified
        self._kwargs.update(kwargs)
        # call mummy reinit
        super(Text, self).reinit(**self._kwargs)
        # ya own reinit
        self._init_base(**self._kwargs)

    def show(self):
        """
        Updates the text
        """
        if self.visible:
            self._text.update_idletasks()

    def _pre_update(self):
        n = len(self._lines_to_insert)
        for i in range(n):
            if self._isempty:
                self._isempty = False
            self._text.insert(self._lines_to_insert[0][0],
                              self._lines_to_insert[0][1])
            self._lines_to_insert.pop(0)

    def add_text(self, txt="", end=None, newline=True, mark_line=None):
        """
        Adds the text ``txt`` to the frame, on a newline if ``newline``
        is ``True``.
        The new ``txt`` is prepended using the format in ``Text.mark_fmt``
        if ``mark_line`` is ``True``, default is ``Text.mark_line``.
        It is added at the end of the frame text if ``rev`` is ``True``,
        default is not(``Text.rev``).
        """
        if not self.visible:
            return
        mark_line = bool(mark_line) \
                        if mark_line is not None else self.mark_line
        if mark_line:
            addon = time.strftime(self.mark_fmt)
        in_the_end = bool(end) if end is not None else not self.rev
        nl_f = "\n" if in_the_end and not self._isempty and newline else ""
        nl_e = "\n" if not in_the_end and not self._isempty and newline else ""
        #self._text._lines_to_
        self._lines_to_insert.append([
            tkinter.END if in_the_end else '1.0',
            "{}{}{}{}".format(nl_f,
                                            addon if mark_line else "",
                                            txt,
                                            nl_e)])

    def clear(self):
        """
        Flushes the text in the frame
        """
        if self.visible:
            self._text.delete('1.0', tkinter.END)
        self._isempty = True
