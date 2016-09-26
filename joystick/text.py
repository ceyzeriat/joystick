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
time = core.time
from .frame import Frame


__all__ = ['Text']


class Text(Frame):
    def __init__(self, daddy, name, freq_up=1, pos=(50, 50), size=(400, 400),
                 screen_relative=False, background="black",
                 foreground='green', rev=True, font=("consolas", 11),
                 mark_line=True, mark_fmt='%H:%M:%S > ', scrollbar=True,
                 **kwargs):
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
        self._rev = bool(kwargs.pop('rev'))
        self._mark_line = bool(kwargs.pop('mark_line'))
        self._mark_fmt = kwargs.pop('mark_fmt')
        self._text = Tkinter.Text(master=self._window, **core.tkkwargs(kwargs))
        self._text.config(font=kwargs.pop('font'),
                          undo=kwargs.pop('undo', True),
                          wrap=kwargs.pop('wrap', 'word'))
        if kwargs.pop('scrollbar'):
            scrollbar = Tkinter.Scrollbar(self._text)
            scrollbar.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
            self._text.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=self._text.yview)
        self._text.pack(side=Tkinter.TOP, fill=Tkinter.BOTH, expand=True)            
        # call the user's init if existing
        core.callit(self, core.INITMETHOD, **kwargs)

    def reinit(self, **kwargs):
        """
        Re-init, closes old and creates new, input params are
        that of the constructor.
        'None' is reuse the previous parameters
        """
        # updates with new reinit value if specified
        self._kwargs.update(kwargs)
        # call mummy reinit
        super(Text, self).reinit(**self._kwargs)
        # ya own reinit
        self._init_base(**self._kwargs)

    def show(self):
        """
        Redraws the graph
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
        if not self.visible:
            return
        mark_line = bool(mark_line) \
                        if mark_line is not None else self._mark_line
        if mark_line:
            addon = time.strftime(self._mark_fmt)
        in_the_end = bool(end) if end is not None else not self._rev
        nl_f = "\n" if in_the_end and not self._isempty and newline else ""
        nl_e = "\n" if not in_the_end and not self._isempty and newline else ""
        #self._text._lines_to_
        self._lines_to_insert.append([
            Tkinter.END if in_the_end else '1.0',
            "{}{}{}{}".format(nl_f,
                                            addon if mark_line else "",
                                            txt,
                                            nl_e)])

    def clear(self):
        if self.visible:
            self._text.delete('1.0',Tkinter.END)
        self._isempty = True
