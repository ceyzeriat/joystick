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
matplotlibpyplotNormalize = core.matplotlibpyplotNormalize


__all__ = ['ColorbarManager']


class ColorbarManager(object):
    def __init__(self, **kwargs):
        self._init_colorbar(**kwargs)
        super(ColorbarManager, self).__init__(**kwargs)

    def _init_colorbar(self, **kwargs):
        self._cmap = kwargs.pop('cmap')
        vmin, vmax = kwargs.pop('vmin'), kwargs.pop('vmax')
        self._vmin = float(vmin) if vmin is not None else None
        self._vmax = float(vmax) if vmax is not None else None
        if vmin is None and vmax is None:
            vmin, vmax = 0, 1  # can't define minmax yet
        elif vmin is None:
            vmin = vmax - self._minmini
        elif vmax is None:
            vmax = vmin + self._minmini
        self._norm = matplotlibpyplotNormalize(vmin, vmax)
        return vmin, vmax
    
    def _reset_colorbar(self, **kwargs):
        vmin, vmax = self._init_colorbar(**kwargs)
        self._set_norm(vmin, vmax)
        self.cmap = kwargs.pop('cmap', self._cmap)

    @property
    def vmin(self):
        """
        The minimum value of the colorbar
        """
        return self._vmin

    @vmin.setter
    def vmin(self, value):
        if value is None:
            self._vmin = None
            value = self.get_data()
            if value is None:
                return
            value = np.min(value) if len(value) > 0 else\
                        (0 if self._vmax is None else self._vmax - 1.0)
        else:
            self._vmin = float(value)
        self._set_norm(value, self._norm.vmax)
        self._update_scalarmappable()
        if not (self.running and self._mummy_running):
            self.show()

    @property
    def vmax(self):
        """
        The maximum value of the colorbar
        """
        return self._vmax

    @vmax.setter
    def vmax(self, value):
        if value is None:
            self._vmax = None
            value = self.get_data()
            if value is None:
                return
            value = np.max(value) if len(value) > 0 else\
                        (1 if self._vmin is None else self._vmin + 1.0)
        else:
            self._vmax = float(value)
        self._set_norm(self._norm.vmin, value)
        if not (self.running and self._mummy_running):
            self.show()

    def _set_norm(self, vmin, vmax):
        self._norm = matplotlibpyplotNormalize(vmin, vmax)
        self._plot.set_norm(self._norm)

    def _update_scalarmappable(self):
        if hasattr(self._plot, 'update_scalarmappable'):
            self._plot.update_scalarmappable()

    @property
    def cmap(self):
        """
        The colormap name
        """
        return self._cmap

    @cmap.setter
    def cmap(self, value):
        # a cm object
        if not isinstance(value, str):
            if hasattr(value, 'name'):
                value = value.name
            else:
                print('Not a valid cmap')
                return
        self._cmap = value
        self._plot.set_cmap(self._cmap)
        self._update_scalarmappable()
        if not (self.running and self._mummy_running):
            self.show()

    def _scale_colors(self):
        """
        Does the color scaling
        """
        # None means recalculate the bound
        if not (self._vmin is None or self._vmax is None):
            return
        colors = self.get_data()
        if (np.size(colors) if colors is not None else 0) == 0:
            return
        vmin = colors.min() if self._vmin is None else self._norm.vmin
        vmax = colors.max() if self._vmax is None else self._norm.vmax
        self._set_norm(vmin, vmax)
