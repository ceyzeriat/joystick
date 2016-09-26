#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#  
#  SOIF - Sofware for Optical Interferometry fitting
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
#    guillaume.schworer@obspm.fr
#
###############################################################################


import numpy as np
import os
from nose.tools import raises

from ..oidata import Oidata
from ..oidataempty import OidataEmpty
from .. import oiexception as exc
from .. import core

def test_create():
    for typ in core.DATAKEYSUPPER:
        oie = OidataEmpty(datatype=typ.lower())
        assert not oie.useit
        oie.useit = True
        assert not oie.useit
        assert not bool(oie)
        assert not oie
        oie._has = True
        assert oie.useit
        assert bool(oie)
        assert oie
        oie.useit = False
        assert not oie.useit
        assert bool(oie)
        assert oie
        assert str(oie) == repr(oie)

def test_getattr():
    oie = OidataEmpty(datatype=core.DATAKEYSUPPER[0])
    assert oie['useit'] == oie.useit
    assert not oie['useit']
    oie.useit = True
    assert oie['useit']
    assert not oie['useit'] == oie.useit

@raises(exc.InvalidDataType)
def test_InvalidDataType():
    oie = OidataEmpty(datatype='random')

def test_InvalidDataType_noraise():
    oie = OidataEmpty(datatype='random', raiseError=False)
    assert not hasattr(oie, '_has')

