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

import os

PAT = os.path.dirname(os.path.abspath(__file__))
PAT = PAT.split(os.path.sep)[:-1]

try:
    __doc__ = """
              {0}
              """.format(open(os.path.join(os.path.sep, os.path.sep.join(PAT), 'README.rst'), 'r').read())
except:
    __doc__ = ""

from .core import *
from .graph import *
from .image import *
from .text import *
from .joystick import *
from .deco import *
from ._version import __version__, __major__, __minor__, __micro__

