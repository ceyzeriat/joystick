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
FigureCanvasTkAgg = core.mat.backends.backend_tkagg.FigureCanvasTkAgg
np = core.np
from .graph import Graph


__all__ = ['GraphMulti']


class GraphMulti(Graph):
    def __init__(self, name, freq_up=1, pos=(50, 50), size=(400, 400),
                 screen_relative=False, xnpts=30, nlines=2, numbering=True,
                 lbls=None, legend=2, fmt=None, bgcol='w',
                 axrect=(0.1, 0.1, 0.9, 0.9), grid='k',
                 xylim=(None, None, None, None), xnptsmax=50, axmargin=(1.1, 1.1),
                  **kwargs):
        """
        Initialises a graph-frame. Use :py:func:`~joystick.graph.Graph.set_xydata` and
        :py:func:`~joystick.graphGraph.get_xydata` to set and get the x- and y-data of the
        graph, or :py:func:`~joystick.graphGraph.set_xylim` and :py:func:`~joystick.graphGraph.get_xylim` to
        get and set the axes limits.

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
          * xnpts (int or None) [optional]: the number of data points to be
            plotted. If ``None``, no limit is applied.
          * nlines (int): the number of lines in the frame
          * numbering (bool) [optional]: whether to display the index of
            the lines near the left-most data-point
          * lbls (list of str) [optional]: the labels to display in the
            legend. Default ``None`` is equivalent to ``['L0', ..., 'Ln-1']``
          * legend (int or False) [optional]: if ``False``: no legend, else
            ``legend`` is its location (0 to 10, see `loc` in plt.legend)
          * fmt (str or list of str) [optional]: the format of the lines as in
            ``plt.plot(x, y, fmt)``. Leave to ``None`` for auto.
          * bgcol (color) [optional]: the background color of the graph
          * axrect (list of 4 floats) [optional]: the axes bounds (l,b,w,h)
            as in ``plt.figure.add_axes(rect=(l,b,w,h))``
          * grid (color or None) [optional]: the grid color, or no grid if
            ``None``
          * xylim (list of 4 floats or None) [optional]: the values of the
            axes limits (xmin, xmax, ymin, ymax), where any value can take
            ``None`` to be recalculated according to the data at each update
          * xnptsmax (int or None) [optional]: the maximum number of data
            points to be recorded, older data points will be deleted. If
            ``None``, no limit is applied.
          * axmargin (tuple of 2 floats) [optional]: a expand factor to
            increase the (x, y) axes limits when they are automatically
            calculated from the data (i.e. some xylim is ``None``)

        Kwargs:
          * Any parameter accepted by ``plt.figure.add_axes`` (eg. ``xlabel``,
            ``ylabel``, ``title``, ``aspect``, etc)
          * Any parameter accepted by ``plt.plot`` (either a single element
            or a list of ``nlines`` elements)
          * Will be passed to the optional custom methods decorated
            with :py:func:`~joystick.deco.deco_callit`
        """
        kwargs['nlines'] = nlines
        kwargs['lbls'] = lbls
        kwargs['legend'] = legend
        kwargs['numbering'] = numbering
        if fmt is None:
            # replicate the basic formating as necessary
            fmt = (core.BASICMULTIFMT
                  * (int(nlines)//len(core.BASICMULTIFMT)+1)
                  )[:int(nlines)]
        super(GraphMulti, self).__init__(name=name, freq_up=freq_up, pos=pos,
                 size=size, screen_relative=screen_relative, xnpts=xnpts,
                 fmt=fmt, bgcol=bgcol, axrect=axrect, grid=grid, xylim=xylim,
                 xnptsmax=xnptsmax, axmargin=axmargin, **kwargs)

    def _init_base(self, **kwargs):
        """
        Separate function from __init__ for re-initialization purpose
        """
        before, after = self._extract_callit('init')
        self._callmthd(before, **kwargs)
        self._init_basic_graph(**kwargs)
        # record multi specific parameters
        self._numbering = bool(kwargs.pop('numbering'))
        self._nlines = int(kwargs.pop('nlines'))
        legend = kwargs.pop('legend')
        self._legend = int(legend) if legend is not False else False
        self.lbls = kwargs.pop('lbls')
        for ith in range(self.nlines):
            self.ax.plot(0, 0,
                         core.get_ith(kwargs.get('fmt'), ith),
                         **core.linekwargs(kwargs, ith))
            if self.numbering:
                self._add_text(ith, 0, 0)
        self._scale_axes()
        self.legend(self._legend is not False, loc=self._legend)
        self._callmthd(after, **kwargs)
        # @@@ remove that soon
        # core.INITMETHOD left for backward compatibility
        if core.INITMETHOD not in after \
            and core.INITMETHOD not in before \
            and hasattr(self, core.INITMETHOD):
            print("DEPRECATION WARNING: You should add the decorator " \
                  "`@_callit('after', 'init')` on `{}`. Refer to example.py" \
                  " ".format(core.INITMETHOD))
            self._callmthd(core.INITMETHOD, **kwargs)

    def _add_text(self, ith, x=None, y=None):
        """
        to add text boxes to the graph
        """
        if x is None or y is None:
            x, y = self.get_xydata(ln=ith)
        self.ax.text(x, y, str(ith), color='w', bbox=dict(color='k', alpha=0.5))

    @property
    def lbls(self):
        """
        The list of labels for the legend (len=
        :py:func:`~joystick.graph.GraphMulti.nlines`)
        Set to ``None`` to simply display ['L0', ..., 'Ln-1'].
        """
        return self._lbls

    @lbls.setter
    def lbls(self, value):
        if value is None:
            self._lbls = ["L"+str(i) for i in range(self.nlines)]
        elif len(value) >= self.nlines:
            self._lbls = list(map(str, list(value)[:self.nlines]))
        else:
            print('lbls should have size {:d}'.format(self.nlines))
            return
        self.legend(self._legend is not False, loc=self._legend)

    def legend(self, show, lbls=[], loc=None, **kwargs):
        """
        Turns the legend on/off interactively

        Args:
          * show (bool): ``True`` or ``False`` whether to display
          * lbls (None or list of str): the labels of the legend.
            See :py:func:`~joystick.graph.GraphMulti.lbls`. Leave to
            ``[]`` for no change in labels
          * loc (int): the location of the legend, as in ``plt.legend``

        Kwargs:
          * Any parameter accepted by ``plt.figure.ax.legend``
        """
        show = bool(show)
        if show:
            if lbls != []:
                self.lbls = lbls
            loc = self._legend if loc is None else int(loc)
            self.ax.legend(self.ax.lines, self.lbls, loc=loc)
        else:
            self.ax.legend_.remove()
        self.show()
    
    @property
    def nlines(self):
        """
        The number of lines in the display
        """
        return self._nlines

    @nlines.setter
    def nlines(self, value):
        print("Read-only.")
    
    @property
    def numbering(self):
        """
        Whether to display the line-boxes on the graph
        """
        return self._numbering

    @numbering.setter
    def numbering(self, value):
        if self._numbering == bool(value):
            return
        self._numbering = bool(value)
        if self._numbering:
            for ith, l in enumerate(self.ax.lines):
                self._add_text(ith)
        else:
            for ith in range(self.nlines):
                self.ax.texts.pop(0)

    def set_xydata(self, x, y, ln=None):
        """
        Sets the x and y data of the graph.
        If ``ln`` is left ``None``, the data of all lines will be set.
        In that case, x and y are expected to be lists (len=
        :py:func:`~joystick.graph.GraphMulti.nlines`) of numpy 1d-vectors.
        
        If ``ln`` is an integer (i.e. line-index), only this line will
        be updated x and y shall be numpy 1d-vectors.

        For each line, only the last :py:func:`~joystick.graph.GraphMulti.xnpts`
        data-points will be displayed
        """
        if not self.visible:
            return
        if ln is not None:
            self._set_data_and_text(ith=int(ln), x=x, y=y)
        else:
            for ith, l in enumerate(self.ax.lines):
                self._set_data_and_text(ith=ith, x=x[ith], y=y[ith])
                        
    def _set_data_and_text(self, ith, x, y):
        """
        set data and move text box if necessary of the ith line
        """
        if self.xnpts is not None:
            self.ax.lines[ith].set_xdata(x[-self.xnpts:])
            self.ax.lines[ith].set_ydata(y[-self.xnpts:])
        else:
            self.ax.lines[ith].set_xdata(x)
            self.ax.lines[ith].set_ydata(y)
        if self.numbering:
            idx = -self.xnpts\
                  if (x.size >= self.xnpts and self.xnpts is not None)\
                  else 0
            xybox= (x[idx], y[idx])\
                   if x.size > 0 and y.size > 0\
                   else (0, 0)
            self.ax.texts[ith].set_position(xybox)
    
    def get_xydata(self, ln=None):
        """
        Returns the x and y data from all lines in the graph:
        ([x1,x2,...], [y1,y2,...]), unless ``ln`` is an integer
        """
        if ln is not None:
            return (self.ax.lines[int(ln)].get_xdata(),
                    self.ax.lines[int(ln)].get_ydata())
        else:
            return ([l.get_xdata() for l in self.ax.lines],
                    [l.get_ydata() for l in self.ax.lines])

    def _get_xydata_minmax(self):
        """
        Just return the min-max bounds of the displayed lines
        """
        x, y = self.get_xydata()
        x = np.concatenate(x)
        y = np.concatenate(y)
        return x.min(), x.max(), y.min(), y.max()
