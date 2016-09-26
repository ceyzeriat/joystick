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

FILENAME = os.path.dirname(os.path.abspath(__file__)) + '/test.oifits'
#FILENAME2 = os.path.dirname(os.path.abspath(__file__)) + '/test2.oifits'
#FILENAME_FULL = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_full.oifits')
#VALIDHDU = 4
#VALIDHDUT3 = 4
#VALIDHDUFAKET3 = 6
#WLHDUT3 = 2
#WLHDU = 3
VALIDTGT = 1

def test_create(seed=42):
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    ans = Oifits(oig.src, datafilter=datafilter)
    assert str(ans) == repr(ans)
    assert ans.vis2
    np.random.seed(seed)
    nums = np.random.random((50))
    assert ans.erb_sigma(nums) == nums
    assert ans.sigma_erb(nums) == nums
    assert ans.systematic_bounds is None
    assert ans.systematic_prior is None
    assert not ans.systematic_fit

@raises(exc.ReadOnly)
def test_ReadOnly_systematic_fit():
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    ans = Oifits(oig.src, datafilter=datafilter)
    ans.systematic_fit = 'random'

def test_ReadOnly_systematic_fit_noraise():
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    ans = Oifits(oig.src, datafilter=datafilter, raiseError=False)
    ans.systematic_fit = 'random'
    assert ans.systematic_fit is not 'random'

@raises(exc.NotCallable)
def test_notcallable_erbsigma():
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    ans = Oifits(oig.src, datafilter=datafilter, erb_sigma=12)

@raises(exc.NotCallable)
def test_notcallable_sigmaerb():
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    ans = Oifits(oig.src, datafilter=datafilter, sigma_erb=12)

def test_notcallable_erbsigma_noraise():
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    ans = Oifits(oig.src, datafilter=datafilter, erb_sigma=12)
    assert not hasatr(ans, 'systematic_bounds')

def test_notcallable_sigmaerb_noraise():
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    ans = Oifits(oig.src, datafilter=datafilter, sigma_erb=12)
    assert not hasatr(ans, 'systematic_bounds')

def test_extract():
    oig = Oigrab(FILENAME)
    ans1 = oig.extract(tgt=VALIDTGT)
    filt = np.asarray([item[1] for item in oig.show_specs(ret=True)[VALIDHDU]]) == VALIDTGT
    ans2 = Oifits(oig.src, datafilter={VALIDHDU: np.arange(DATASETSIZE)[filt]+1})
    assert np.allclose(ans1.vis2.data, ans2.vis2.data)

