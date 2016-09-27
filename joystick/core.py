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

import matplotlib as mat
mat.use('TkAgg')
from matplotlib import lines
from matplotlib.backends import backend_tkagg
import matplotlib.cm
from matplotlib.pyplot import Normalize as matplotlibpyplotNormalize
try:
    import Tkinter as tkinter
except ImportError:
    import tkinter
import time
import numpy as np


__all__ = []


# la méthode d'initialisation des graphes
INITMETHOD = "_init"
# la méthode de mise à jour des graphes
UPDATEMETHOD = "_update"
PREUPDATEMETHOD = "_pre_update"
# la méthode de mise à jour de la GUI
UPDATEGUIMETHOD = "show"
# nombre de pts gardés en mémoire en X

doc_cst = {'INITMETHOD': INITMETHOD,
           'UPDATEMETHOD': UPDATEMETHOD}
__doc__ = """Here are some useful constants:

             .. py:data:: INITMETHOD

                = '_init'

             .. py:data:: UPDATEMETHOD

                = '_update'
          """


MATKWARGS = [item[4:] \
                for item in mat.lines.Line2D.__dict__.keys() \
                if 'set_' in item]


TKKWARGS = ['background', 'borderwidth', 'cursor', 'exportselection', 'font',
            'foreground', 'highlightbackground', 'highlightcolor',
            'highlightthickness', 'insertbackground', 'insertborderwidth',
            'insertofftime', 'insertontime', 'insertwidth', 'padx', 'pady',
            'relief', 'selectbackground', 'selectborderwidth',
            'selectforeground', 'setgrid', 'takefocus', 'xscrollcommand',
            'yscrollcommand']


def cm_bounds_to_norm(cm_bounds, data=None):
    cmin = float(cm_bounds[0]) if cm_bounds[0] is not None \
               else (np.min(data) if data is not None else 0)
    cmax = float(cm_bounds[1]) if cm_bounds[1] is not None \
               else (np.max(data) if data is not None else cmin+1)
    return matplotlibpyplotNormalize(cmin, cmax)


def colorbar(cmap="jet", cm_bounds=(0, 1)):
    """
    cmap, norm, mappable = colorbar('jet', min, max)
    plt.scatter(x, y, c, cmap=cmap, norm=norm)
    cb = plt.colorbar(mappable)
    if arr is given, forces cm_min and cm_max to min-max of the arr
    """
    if isinstance(cmap, str):
        cmap = mat.cm.get_cmap(cmap)
    cmin, cmax = list(map(float, cm_bounds[:2]))
    norm = matplotlibpyplotNormalize(cmin, cmax)
    mappable = mat.cm.ScalarMappable(cmap=cmap, norm=norm)
    mappable._A = []
    return cmap, norm, mappable


def matkwargs(kwargs):
    """
    Returns a copy of kwargs that contains only keys existing
    to matplotlib
    """
    return extract_kwargs(kwargs, MATKWARGS)


def tkkwargs(kwargs):
    """
    Returns a copy of kwargs that contains only keys existing
    to tkinter
    """
    return extract_kwargs(kwargs, TKKWARGS)


def extract_kwargs(kwargs, ll):
    """
    Returns a copy of kwargs that contains only keys found in ll
    """
    dic = {}
    for key, v in kwargs.items():
        if key in ll:
            dic[key] = v
    return dic


def callit(self, methodstr, *args, **kwargs):
    """
    Calls self.'methodstr' after having tests that it exists and that
    it is callable
    """
    if callable(getattr(self, methodstr, None)):
        return getattr(self, methodstr)(*args, **kwargs)


def add_datapoint(ar, ar2, xnptsmax=None):
    """
    Concatenates ar2 to ar (either int/float or 1-dim vectors)
    Optionally, 
    """
    if xnptsmax is None:
        return np.r_[ar, ar2]
    else:
        return np.r_[ar[-int(xnptsmax)+np.size(ar2):], ar2]


def timestamp():
    """
    time.time()
    """
    return time.time()


def append(self, attr, v):
    """
    Appends v to self.'attr' (creates an empty list if it does not
        exist yet)
    """
    if hasattr(self, attr):
        getattr(self, attr).append(v)
    else:
        setattr(self, attr, [v])


class font:
    white = '\033[97m'
    black = '\033[38;5;16m'
    gray = '\033[90m'
    red = '\033[31m'
    green = '\033[32m'
    yellow = '\033[33m'
    orange = '\033[38;5;166m'
    blue = '\033[34m'
    magenta = '\033[35m'
    nocolor = '\033[39m'
    bold = '\033[1m'
    nobold = '\033[21m'
    underlined = '\033[4m'
    nounderlined = '\033[24m'
    dim = '\033[2m'
    nodim = '\033[22m'
    normal = nodim + nobold + nobold + nocolor
    clear = chr(27)+"[2J"

    @staticmethod
    def pos(line, col):
        return "\033[{};{}H".format(int(line), int(col))
