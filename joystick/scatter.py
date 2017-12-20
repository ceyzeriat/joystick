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
from .graph import Graph
from .colorbarmanager import ColorbarManager


__all__ = ['Scatter']


class Scatter(ColorbarManager, Graph):
    def __init__(self, name, freq_up=1, pos=(50, 50), size=(400, 400),
                 screen_relative=False, xnpts=30, c='r', s=20,
                 bgcol='w', axrect=(0.1, 0.1, 0.9, 0.9), grid='k',
                 xylim=(None, None, None, None), xnptsmax=50, axmargin=(1.1, 1.1),
                 cmap='gist_earth', vmin=None, vmax=None, **kwargs):
                 
        """
        Initialises a graph-frame. Use
        :py:func:`~joystick.graph.Graph.set_xydata` and
        :py:func:`~joystick.graphGraph.get_xydata` to set and get the x- and
        y-data of the graph, or :py:func:`~joystick.graphGraph.set_xylim` and
        :py:func:`~joystick.graphGraph.get_xylim` to get and set the axes
        limits.

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
          * c (color, sequence, or sequence of color): the color of the
            markers, as in ``plt.scatter``.
          * s (scalar or vector): the size of the markers, as in
            ``plt.scatter``
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
          * cmap (str or colormap): the colormap of the scatter colors
          * vmin (float or None): the value corresponding to the min of
            the colorbar, or ``None`` for auto-scaling
          * vmax (float or None): the value corresponding to the max of
            the colorbar, or ``None`` for auto-scaling

        Kwargs:
          * Any non-abbreviated parameter accepted by ``figure.add_axes``
            (eg. ``xlabel``, ``ylabel``, ``title``, ``aspect``) and
            ``plt.scatter``
          * Will be passed to the optional custom methods decorated
            with :py:func:`~joystick.deco.deco_callit`
        """
        kwargs['c'] = c
        kwargs['s'] = s
        kwargs['cmap'] = cmap
        kwargs['vmin'] = vmin
        kwargs['vmax'] = vmax
        self._kwargs = kwargs
        super(Scatter, self).__init__(name=name, freq_up=freq_up, pos=pos,
                 size=size, screen_relative=screen_relative, xnpts=xnpts,
                 bgcol=bgcol, axrect=axrect, grid=grid, xylim=xylim,
                 xnptsmax=xnptsmax, axmargin=axmargin, **self._kwargs)
        self._preupdate_fcts += ['_scale_colors']

    def _init_base(self, **kwargs):
        """
        Separate function from __init__ for re-initialization purpose
        """
        before, after = self._extract_callit('init')
        # callfront
        self._callmthd(before, **kwargs)
        self._init_basic_graph(**kwargs)
        # record scatter specific parameters
        self._c = kwargs.pop('c')
        self._s = kwargs.pop('s')
        self._plot = self.ax.scatter(0, 0, c=self._c, vmin=self.vmin,
                                        vmax=self.vmax, s=self._s,
                                        cmap=self.cmap,
                                        **core.scatkwargs(kwargs))
        self._reset_colorbar(**kwargs)
        self._scale_axes(force=True)
        # callbacks
        self._callmthd(after, **kwargs)

    @property
    def s(self):
        """
        Size attribute of scatter markers
        """
        return self._s

    @s.setter
    def s(self, value):
        if not hasattr(value, '__iter__'):
            self._s = value
            self._plot.set_sizes([self._s])
        if not (self.running and self._mummy_running):
            self.show()

    @property
    def c(self):
        """
        Color attribute of scatter markers
        """
        return self._c

    @c.setter
    def c(self, value):
        if not hasattr(value, '__iter__'):
            self._c = np.asarray(value)
            self._plot.set_array(self._c)
            self._update_scalarmappable()
        if not (self.running and self._mummy_running):
            self.show()

    def _get_xydata_minmax(self):
        res = self._plot.get_offsets()
        if (0 if res is None else np.size(res)) == 0:
            return self.get_xylim()
        return np.min(res[:,0]), np.max(res[:,0]), np.min(res[:,1]), np.max(res[:,1])

    def get_data(self):
        """
        Returns the color-encoded values of the markers
        """
        return self._plot.get_array()

    def set_data(self, value):
        """
        Sets the color-encoded values of the markers
        """
        self._plot.set_sizes(np.asarray(value)[-self.xnpts:])

    def get_xydata(self):
        """
        Returns the (x, y, c, s) data of the scatter points
        """
        res = self._plot.get_offsets()
        sz = self._plot.get_sizes()
        cl = self.get_data()
        return res[:,0], res[:,1], sz, cl

    def set_xydata(self, x, y, c=None, s=None):
        """
        Sets the x, y, c and s data of the markers.
        Only the last :py:func:`~joystick.graph.Scatter.xnpts`
        data-points will be displayed
        """
        if not self.visible:
            return
        xy = np.asarray([x,y]).T
        if self.xnpts is not None:
            self._plot.set_offsets(xy[-self.xnpts:])
            if c is not None:
                self._plot.set_array(np.asarray(c)[-self.xnpts:])
                self._update_scalarmappable()
            if s is not None:
                self.set_data(s)
        else:
            self._plot.set_offsets(xy)
