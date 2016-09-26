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
from ..oifits import Oifits
from ..oigrab import Oigrab
from .. import oiexception as exc

FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test.oifits')
FILENAME_NOTARGET = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_notarget.oifits')
FILENAME_NOWL = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_nowl.oifits')
FILENAME_FULL = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_full.oifits')
VALIDHDU = 4
T3HDU = 6
DATASETSIZE = 12
VALIDTGT = 1

def test():
    oig = Oigrab(FILENAME)
    assert len(oig.targets) == 3
    assert oig.targets[0] == 'HD_204770'
    assert str(oig) == repr(oig)

@raises(exc.NoTargetTable)
def test_NoTargetTable():
    oig = Oigrab(FILENAME_NOTARGET)

def test_NoTargetTable_noraise():
    oig = Oigrab(FILENAME_NOTARGET, raiseError=False)
    assert not hasattr(oig, '_targets')

@raises(exc.NoWavelengthTable)
def test_NoWavelengthTable():
    oig = Oigrab(FILENAME_NOWL)

def test_NoWavelengthTable_noraise():
    oig = Oigrab(FILENAME_NOWL, raiseError=False)

@raises(exc.ReadOnly)
def test_readonly_attribute():
    oig = Oigrab(FILENAME)
    oig.targets = []

def test_show_specs():
    oig = Oigrab(FILENAME)
    ans = oig.show_specs(ret=False)
    ans = oig.show_specs(ret=True)
    for item in range(10):
        if item != VALIDHDU:
            assert ans.get(item) is None
    assert len(ans[VALIDHDU]) == DATASETSIZE
    assert np.allclose(ans[VALIDHDU][0], (0, 0, 57190.4437, 1, 38))
    assert (np.diff([item[2] for item in ans[VALIDHDU]]) >= 0).all()

def test_filtered():
    oig = Oigrab(FILENAME)
    for item in range(10):
        if item != VALIDHDU:
            assert oig.filtered(tgt=VALIDTGT, verbose=True).get(item) is None
        else:
            assert oig.filtered(tgt=VALIDTGT, verbose=True).get(item).tolist() == [ 2,  5,  8, 11]
    oig = Oigrab(FILENAME_FULL)
    ans = oig.filtered(tgt=VALIDTGT, verbose=True)
    assert len(ans) == 5
    assert len(ans[VALIDHDU]) == 4
    assert len(ans[T3HDU]) == 140
    assert len(oig.filtered(tgt=VALIDTGT, hdus=(VALIDHDU,T3HDU), verbose=True)) == 3
    ans = oig.filtered(tgt=VALIDTGT, hdus=(T3HDU), t3amp=False, mjd=(55636.3382228, 55636.3396117), verbose=True)
    assert len(ans) == 2
    assert ans['data']['T3AMP'] == False
    assert ans[T3HDU].min() == 70
    assert ans[T3HDU].max() == 174
    assert len(ans[T3HDU]) == 70
