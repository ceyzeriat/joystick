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
import Tkinter
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
XNPTSMAX = 50


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


def matkwargs(kwargs):
    return extract_kwargs(kwargs, MATKWARGS)


def tkkwargs(kwargs):
    return extract_kwargs(kwargs, TKKWARGS)


def extract_kwargs(kwargs, ll):
    dic = {}
    for key, v in kwargs.items():
        if key in ll:
            dic[key] = v
    return dic


def callit(self, methodstr, *args, **kwargs):
    if callable(getattr(self, methodstr, None)):
        return getattr(self, methodstr)(*args, **kwargs)


def add_datapoint(ar, ar2):
        return np.r_[ar[-XNPTSMAX+np.size(ar2):], ar2]


def timestamp():
    return time.time()


def append(self, attr, v):
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
