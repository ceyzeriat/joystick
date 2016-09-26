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
FigureCanvasTkAgg = core.mat.backends.backend_tkagg.FigureCanvasTkAgg
np = core.np
from .frame import Frame


__all__ = ['Graph']


class Graph(Frame):
    def __init__(self, daddy, name, freq_up=1, pos=(50, 50), size=(400, 400),
                 screen_relative=False, xnpts=core.XNPTSMAX, fmt="ro-",
                 bgcol='w', axrect=(0.1, 0.1, 0.9, 0.9), grid='k',
                 xylim=(0., None, 0., None), **kwargs):
        """
        Initialization
        """
        kwargs['daddy'] = daddy
        kwargs['name'] = name
        kwargs['freq_up'] = freq_up
        kwargs['pos'] = pos
        kwargs['size'] = size
        kwargs['screen_relative'] = screen_relative
        kwargs['xnpts'] = xnpts
        kwargs['fmt'] = fmt
        kwargs['bgcol'] = bgcol
        kwargs['axrect'] = axrect
        kwargs['grid'] = grid
        kwargs['xylim'] = xylim
        self._minmini = 1e-2
        self._kwargs = kwargs
        # call mummy init
        super(Graph, self).__init__(**self._kwargs)
        # call ya own init
        self._init_base(**self._kwargs)

    def _init_base(self, **kwargs):
        self.xylim = tuple(kwargs.pop('xylim')[:4])
        self.xnpts = int(kwargs.pop('xnpts'))
        axrect = tuple(kwargs.pop('axrect')[:4])
        self._fig = core.mat.figure.Figure()
        self.ax = self._fig.add_axes(axrect[:2] + (axrect[2]-axrect[0],
                                                   axrect[3]-axrect[1]),
                                     **core.matkwargs(kwargs))
        self._canvas = FigureCanvasTkAgg(self._fig, master=self._window)
        self._canvas.show()
        self._canvas.get_tk_widget().pack(side=Tkinter.TOP,
                                          fill=Tkinter.BOTH,
                                          expand=True)
        self._canvas._tkcanvas.pack(side=Tkinter.TOP,
                                    fill=Tkinter.BOTH,
                                    expand=True)
        self.ax.set_axis_bgcolor(kwargs.pop('bgcol'))
        grid = kwargs.pop('grid')
        if grid not in [None, False]:
            self.ax.grid(color=grid, lw=1)
        self.ax.plot(0, 0, kwargs.pop('fmt'), **core.matkwargs(kwargs))
        core.callit(self, core.PREUPDATEMETHOD)
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
        super(Graph, self).reinit(**self._kwargs)
        # ya own reinit
        self._init_base(**self._kwargs)

    def show(self):
        """
        Redraws the graph
        """
        if self.visible:
            self._canvas.draw()

    @property
    def xnpts(self):
        return self._xnpts

    @xnpts.setter
    def xnpts(self, value):
        if not 1 < value <= core.XNPTSMAX:
            print("{}Invalid value. Must be 1--{}{}" \
            .format(core.font.red, core.XNPTSMAX, core.font.normal))
            return
        self._xnpts = int(value)

    def set_xydata(self, x, y):
        """
        Give x and y raw vectors
        """
        if self.visible:
            self.ax.lines[0].set_xdata(x[-self.xnpts:])
            self.ax.lines[0].set_ydata(y[-self.xnpts:])

    def get_xydata(self):
        """
        Give x and y raw vectors
        """
        if self.visible:
            return self.ax.lines[0].get_xdata(), self.ax.lines[0].get_ydata()

    def set_xylim(self, xylim=(None, None, None, None)):
        if not self.visible:
            return
        xmin, xmax, ymin, ymax = xylim
        xmin_o, xmax_o, ymin_o, ymax_o = self.get_xylim()
        xmin = xmin_o if xmin is None else float(xmin)
        xmax = xmax_o if xmax is None else float(xmax)
        ymin = ymin_o if ymin is None else float(ymin)
        ymax = ymax_o if ymax is None else float(ymax)
        if not np.allclose([xmin, xmax], [xmin_o, xmax_o]):
            self.ax.set_xlim([xmin, xmax])
        if not np.allclose([ymin, ymax], [ymin_o, ymax_o]):
            self.ax.set_ylim([ymin, ymax])

    def get_xylim(self):
        if self.visible:
            return self.ax.get_xlim() + self.ax.get_ylim()

    def _pre_update(self):
        x, y = self.get_xydata()
        # None means recalculate the bound
        xmin, xmax, ymin, ymax = self.xylim
        xmin = x.min() if xmin is None else xmin
        xmax = max(x.max(), xmin+self._minmini) if xmax is None else xmax
        ymin = y.min() if ymin is None else ymin
        ymax = max(y.max(), ymin+self._minmini) if ymax is None else ymax
        self.set_xylim((xmin, xmax, ymin, ymax))
