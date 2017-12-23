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
from .frame import Frame


__all__ = ['Graph']


class Graph(Frame):
    def __init__(self, name, freq_up=1, pos=(50, 50), size=(400, 400),
                 screen_relative=False, xnpts=30, fmt="ro-", bgcol='w',
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
          * fmt (str) [optional]: the format of the line as in
            ``plt.plot(x, y, fmt)``
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
          * Any non-abbreviated parameter accepted by ``figure.add_axes``
            (eg. ``xlabel``, ``ylabel``, ``title``, ``aspect``) and ``plt.plot``
          * Will be passed to the optional custom methods decorated
            with :py:func:`~joystick.deco.deco_callit`
        """
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
        kwargs['xnptsmax'] = xnptsmax
        kwargs['axmargin'] = axmargin
        self._minmini = 1e-2
        self._kwargs = kwargs
        # call mummy init
        super(Graph, self).__init__(**self._kwargs)
        self._preupdate_fcts += ['_scale_axes']
        # call ya own init
        self._init_base(**self._kwargs)

    def _init_base(self, **kwargs):
        """
        Separate function from __init__ for re-initialization purpose
        """
        before, after = self._extract_callit('init')
        self._callmthd(before, **kwargs)
        self._init_basic_graph(**kwargs)
        self._plot, = self.ax.plot(0, 0, kwargs.pop('fmt'),
                                  **core.linekwargs(kwargs))
        self._scale_axes(force=True)
        self._callmthd(after, **kwargs)

    def _init_basic_graph(self, **kwargs):
        self._xylim = tuple(kwargs.pop('xylim')[:4])
        self._axmargin = tuple(map(abs, kwargs.pop('axmargin')[:2]))
        self._xnpts = int(kwargs.pop('xnpts'))
        self._xnptsmax = max(int(kwargs.pop('xnptsmax')), self.xnpts)
        axrect = tuple(kwargs.pop('axrect')[:4])
        self._fig = core.mat.figure.Figure()
        self.ax = self._fig.add_axes(axrect[:2] + (axrect[2]-axrect[0],
                                                   axrect[3]-axrect[1]),
                                     **core.axkwargs(kwargs))
        self._canvas = FigureCanvasTkAgg(self._fig, master=self._window)
        self._canvas.show()
        self._canvas.get_tk_widget().pack(side=tkinter.TOP,
                                          fill=tkinter.BOTH,
                                          expand=True)
        self._canvas._tkcanvas.pack(side=tkinter.TOP,
                                    fill=tkinter.BOTH,
                                    expand=True)
        bgcol = kwargs.pop('bgcol')
        try:  # for matplotlib >2.0
            self.ax.set_facecolor(bgcol)
        except AttributeError:  # for matplotlib <1.5
            self.ax.set_axis_bgcolor(bgcol)
        grid = kwargs.pop('grid')
        if grid not in [None, False]:
            self.ax.grid(color=grid, lw=1)

    def add_datapoint(self, data=None, new_data=None, data1=None, data2=None):
        if data is None and data1 is not None and new_data is None\
                and data2 is not None:
            print("DEPRECATION: use data and new_data keyword instead of "\
                  "data1 and data2")
            data, new_data = data1, data2
        return core.add_datapoint(data, new_data, xnptsmax=self.xnptsmax)

    def reinit(self, **kwargs):
        """
        Re-initializes the frame, i.e. closes the current frame if
        necessary and creates a new one. Uses the parameters of
        initialization by default or anything provided through kwargs.
        See class :py:class:`~joystick.graph.Graph` for the description of input parameters.
        """
        # updates with new reinit value if specified
        self._kwargs.update(kwargs)
        # call mummy reinit
        super(Graph, self).reinit(**self._kwargs)
        # ya own reinit
        self._init_base(**self._kwargs)

    def show(self):
        """
        Updates the graph
        """
        if self.visible:
            self._canvas.draw()

    @property
    def xnptsmax(self):
        """
        The maximum number of data points to be recorded, older data
        points will be deleted. Must be > 1.
        If ``None``, no limit is applied.
        """
        return self._xnptsmax

    @xnptsmax.setter
    def xnptsmax(self, value):
        if value is None:
            self._xnptsmax = None
        elif value >= 1:
            self._xnptsmax = int(value)
        else:
            print("{}Invalid value. Must be > 1{}" \
            .format(core.font.red, core.font.normal))

    @property
    def xnpts(self):
        """
        The number of data points to be plotted. Must be
        1 < xnpts <= ``Graph.xnptsmax``.
        If ``None``, no limit is applied.
        """
        return self._xnpts

    @xnpts.setter
    def xnpts(self, value):
        if value is None:
            self._xnpts = None
        elif 1 < value <= self.xnptsmax:
            self._xnpts = int(value)
        else:
            print("{}Invalid value. Must be 1--{}{}" \
            .format(core.font.red, self.xnptsmax, core.font.normal))

    def set_xydata(self, x, y):
        """
        Sets the x and y data of the graph.
        Give x and y vectors as numpy arrays; only the last
        :py:func:`~joystick.graph.Graph.xnpts` data-points will be displayed
        """
        if self.visible:
            if self.xnpts is not None:
                self._plot.set_xdata(x[-self.xnpts:])
                self._plot.set_ydata(y[-self.xnpts:])
            else:
                self._plot.set_xdata(x)
                self._plot.set_ydata(y)

    def get_xydata(self):
        """
        Returns the x and y data of the graph
        """
        if self.visible:
            return self._plot.get_xdata(), self._plot.get_ydata()

    def _get_xydata_minmax(self):
        ret = self.get_xydata()
        # graph not visible
        if ret is None:
            return
        x, y = ret
        # if no data on the graph, just return None
        if (0 if x is None else x.size) == 0 or (0 if y is None else y.size) == 0:
            return None
        return np.min(x), np.max(x), np.min(y), np.max(y)

    @property
    def axmargin(self):
        return self._axmargin

    @axmargin.setter
    def axmargin(self, value):
        if len(value) != 2:
            print("Wrong size for axmargin, should be 2")
        else:
            self._axmargin = list(map(float, value))
            if not (self.running and self._mummy_running):
                self.show()

    @property
    def xylim(self):
        return self._xylim

    @xylim.setter
    def xylim(self, value):
        """
        The (xmin, xmax, ymin, ymax) limits of the graph
        """
        if len(value) != 4:
            print("Wrong size for xylim, should be 4")
        else:
            self._xylim = [float(item) if item is not None else None\
                           for item in value]
            self._scale_axes(force=True)
            if not (self.running and self._mummy_running):
                self.show()

    def set_xylim(self, xylim=(None, None, None, None)):
        """
        DEPRECATED, use `xylim = (.., .., .., ..)` instead
        """
        print("DEPRECATED, use `xylim = (.., .., .., ..)` instead")
        self._set_xylim(xylim=xylim)

    def _set_xylim(self, xylim=(None, None, None, None)):
        if not self.visible:
            return
        if len(xylim) != 4:
            print("Wrong xylim size, should be 4")
            return
        xmin, xmax, ymin, ymax = xylim[:4]
        xmin_o, xmax_o, ymin_o, ymax_o = self.get_xylim_graph()
        xmin = xmin_o if xmin is None else float(xmin)
        xmax = xmax_o if xmax is None else float(xmax)
        ymin = ymin_o if ymin is None else float(ymin)
        ymax = ymax_o if ymax is None else float(ymax)
        if not np.allclose([xmin, xmax], [xmin_o, xmax_o]):
            self.ax.set_xlim([xmin, xmax])
        if not np.allclose([ymin, ymax], [ymin_o, ymax_o]):
            self.ax.set_ylim([ymin, ymax])

    def get_xylim(self):
        """
        DEPRECATED, use `get_xylim_graph()` method instead
        """
        print("DEPRECATED, use `get_xylim_graph()` method instead")
        return self.get_xylim_graph()

    def get_xylim_graph(self):
        """
        Returns the (xmin, xmax, ymin, ymax) limits of the actual
        graph object as of the time of call
        """
        if self.visible:
            return self.ax.get_xlim() + self.ax.get_ylim()

    def _scale_axes(self, force=False):
        """
        Does the axes scaling given the xylim property
        """
        # None means recalculate the bound
        xmin, xmax, ymin, ymax = self.xylim[:4]
        if not (xmin is None or xmax is None
                or ymin is None or ymax is None or force):
            return
        ret = self._get_xydata_minmax()
        # no data on graph, no need to update the axes
        if ret is None:
            return
        xmin_f, xmax_f, ymin_f, ymax_f = ret
        xmin_f = xmin_f if xmin is None else xmin
        xmax_f = max(xmax_f, xmin_f+self._minmini) if xmax is None else xmax
        ymin_f = ymin_f if ymin is None else ymin
        ymax_f = max(ymax_f, ymin_f+self._minmini) if ymax is None else ymax
        if self.axmargin[0] != 1.0:
            dx = (self.axmargin[0]-1)*(xmax_f-xmin_f)*0.5
            if xmin is None:
                xmin_f -= dx
            if xmax is None:
                xmax_f += dx
        if self.axmargin[1] != 1.0:
            dy = (self.axmargin[1]-1)*(ymax_f-ymin_f)*0.5
            if ymin is None:
                ymin_f -= dy
            if ymax is None:
                ymax_f += dy
        self._set_xylim((xmin_f, xmax_f, ymin_f, ymax_f))

    def savefig(fname, *args, **kwargs):
        """
        Saves the current figure to file

        See matplotlib.figure.Figure.savefig for details
        """
        return self._fig.savefig(fname, *args, **kwargs)
