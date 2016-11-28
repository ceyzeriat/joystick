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
matplotlibpyplotNormalize = core.matplotlibpyplotNormalize
from .graph import Graph


__all__ = ['Scatter']


class Scatter(Graph):
    def __init__(self, name, freq_up=1, pos=(50, 50), size=(400, 400),
                 screen_relative=False, xnpts=30, c='r', s=20,
                 bgcol='w', axrect=(0.1, 0.1, 0.9, 0.9), grid='k',
                 xylim=(0., None, 0., None), xnptsmax=50, axmargin=(1.1, 1.1),
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
            (eg. ``xlabel``, ``ylabel``, ``title``, aspect``) and
            ``plt.scatter``
          * Will be passed to the optional custom methods decorated
            with :py:func:`~joystick.deco.deco_callit`
        """
        kwargs['c'] = c
        kwargs['s'] = s
        kwargs['cmap'] = cmap
        kwargs['vmin'] = vmin
        kwargs['vmax'] = vmax
        super(Scatter, self).__init__(name=name, freq_up=freq_up, pos=pos,
                 size=size, screen_relative=screen_relative, xnpts=xnpts,
                 bgcol=bgcol, axrect=axrect, grid=grid, xylim=xylim,
                 xnptsmax=xnptsmax, axmargin=axmargin, **kwargs)
        self._preupdate_fcts += ['_scale_colors']

    def _init_base(self, **kwargs):
        """
        Separate function from __init__ for re-initialization purpose
        """
        before, after = self._extract_callit('init')
    
        self._callmthd(before, **kwargs)
        self._init_basic_graph(**kwargs)
        # record scatter specific parameters
        self._c = kwargs.pop('c')
        self._s = kwargs.pop('s')
        self._cmap = kwargs.pop('cmap')
        vmin, vmax = kwargs.pop('vmin'), kwargs.pop('vmax')
        self._vmin = float(vmin) if vmin is not None else None
        self._vmax = float(vmax) if vmax is not None else None
        if vmin is None and vmax is None:
            vmin, vmax = 0, 1  # can't define minmax yet
        elif vmin is None:
            vmin = vmax-self._minmini
        elif vmax is None:
            vmax = vmin+self._minmini
        self._norm = matplotlibpyplotNormalize(vmin, vmax)
        self._scatter = self.ax.scatter(0, 0, c=self._c, vmin=vmin,
                                        vmax=vmax, s=self._s,
                                        cmap=self._cmap,
                                        **core.linekwargs(kwargs))
        self._scale_axes()
        # callbacks
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

    @property
    def vmin(self):
        return self._vmin

    @vmin.setter
    def vmin(self, value):
        if value is None:
            value = self._scatter.get_array().min()
            self._vmin = None
        else:
            self._vmin = float(value)
        self._set_norm(float(value), self._norm.vmax)

    @property
    def vmax(self):
        return self._vmax

    @vmax.setter
    def vmax(self, value):
        if value is None:
            value = self._scatter.get_array().max()
            self._vmax = None
        else:
            self._vmax = float(value)
        self._set_norm(self._norm.vmin, float(value))

    @property
    def s(self):
        return self._s

    @s.setter
    def s(self, value):
        if not hasattr(value, '__iter__'):
            self._s = value
            self._scatter.set_sizes([self._s])

    @property
    def c(self):
        return self._c

    @c.setter
    def c(self, value):
        if not hasattr(value, '__iter__'):
            self._c = np.asarray(value)
            self._scatter.set_array(self._c)
            self._scatter.update_scalarmappable()

    def _set_norm(self, vmin, vmax):
        self._norm = matplotlibpyplotNormalize(vmin, vmax)
        self._scatter.set_norm(self._norm)
        self._scatter.update_scalarmappable()


    @property
    def cmap(self):
        """
        The colormap of the scatter points
        """
        return self._cmap

    @cmap.setter
    def cmap(self, value):
        # a cm object
        if not isinstance(value, str):
            if hasattr(value, 'name'):
                value = value.name
            else:
                print('Not a value cmap')
                return
        self._scatter.set_cmap(value)
        self._scatter.update_scalarmappable()
        self._cmap = value

    def _scale_colors(self):
        """
        Does the color scaling
        """
        # None means recalculate the bound
        if not (self._vmin is None or self._vmax is None):
            return
        colors = self._scatter.get_array()
        vmin = colors.min() if self._vmin is None else self._norm.vmin
        vmax = colors.max() if self._vmax is None else self._norm.vmax
        self._set_norm(vmin, vmax)

    def _get_xydata_minmax(self):
        res = self._scatter.get_offsets()
        return np.min(res[:,0]), np.max(res[:,0]), np.min(res[:,1]), np.max(res[:,1])

    def get_xydata(self):
        """
        Returns the (x, y, c, s) data of the scatter points
        """
        res = self._scatter.get_offsets()
        sz = self._scatter.get_sizes()
        cl = self._scatter.get_array()
        return res[:,0], res[:,1], sz, cl

    def set_xydata(self, x, y, c=None, s=None):
        """
        Sets the x, y, c and s data of the points.
        Only the last :py:func:`~joystick.graph.Scatter.xnpts`
        data-points will be displayed
        """
        if not self.visible:
            return
        xy = np.asarray([x,y]).T
        if self.xnpts is not None:
            self._scatter.set_offsets(xy[-self.xnpts:])
            if c is not None:
                self._scatter.set_array(np.asarray(c)[-self.xnpts:])
                self._scatter.update_scalarmappable()
            if s is not None:
                self._scatter.set_sizes(np.asarray(s)[-self.xnpts:])
        else:
            self._scatter.set_offsets(xy)
