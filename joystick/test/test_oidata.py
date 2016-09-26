#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
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
################################################################################


import numpy as np
import os
from nose.tools import raises

from ..oidata import Oidata
from ..oigrab import Oigrab
from ..oidataempty import OidataEmpty
from ..oifits import Oifits
from .. import oiexception as exc

FILENAME = os.path.dirname(os.path.abspath(__file__)) + '/test.oifits'
FILENAME2 = os.path.dirname(os.path.abspath(__file__)) + '/test2.oifits'
FILENAME_FULL = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_full.oifits')
VALIDHDU = 4
VALIDHDUT3 = 4
VALIDHDUFAKET3 = 6
WLHDUT3 = 2
WLHDU = 3
VALIDTGT = 1


def test_create():
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    oid = Oidata(src=FILENAME, hduidx=VALIDHDU, datatype="VIS2", hduwlidx=WLHDU, indices=datafilter[VALIDHDU])
    assert oid.flat == False
    assert str(oid) == repr(oid)
    assert oid
    assert bool(oid)
    oid.useit = False
    assert oid
    assert bool(oid)
    assert not oid.useit
    assert oid.shapedata == (4,38)
    assert oid.shapedata == oid.shapeuv
    assert oid.data.shape == oid.shapedata
    assert oid.error.shape == oid.shapedata
    assert oid.wl.shape == oid.shapedata
    assert oid.wl_d.shape == oid.shapedata
    assert oid.u.shape == oid.shapedata
    assert oid.v.shape == oid.shapedata
    assert oid.pa.shape == oid.shapedata
    assert oid.bl.shape == oid.shapedata
    assert oid.blwl.shape == oid.shapedata
    oid.flatten()
    assert oid.flat == True
    assert oid.shapedata == (152,)
    assert oid.shapedata == oid.shapeuv
    assert oid.data.shape == oid.shapedata
    assert oid.error.shape == oid.shapedata
    assert oid.wl.shape == oid.shapedata
    assert oid.wl_d.shape == oid.shapedata
    assert oid.u.shape == oid.shapedata
    assert oid.v.shape == oid.shapedata
    assert oid.pa.shape == oid.shapedata
    assert oid.bl.shape == oid.shapedata
    assert oid.blwl.shape == oid.shapedata
    oid = Oidata(src=FILENAME, hduidx=VALIDHDU, datatype="VIS2", hduwlidx=WLHDU, indices=datafilter[VALIDHDU], flatten=True)
    assert oid.shapedata == (152,)


def test_create_T3():
    oig = Oigrab(FILENAME2)
    datafilter = oig.filtered(tgt=VALIDTGT, t3amp=False)
    oid = Oidata(src=FILENAME2, hduidx=VALIDHDUT3, datatype="T3PHI", hduwlidx=WLHDUT3, indices=datafilter[VALIDHDUT3])
    assert str(oid) == repr(oid)
    assert oid
    assert bool(oid)
    oid.useit = False
    assert oid
    assert bool(oid)
    assert not oid.useit
    assert len(oid.shapedata) == 2
    assert len(oid.shapeuv) == 3
    assert oid.shapeuv[-1] == 3
    assert oid.data.shape == oid.shapedata
    assert oid.error.shape == oid.shapedata
    assert oid.wl.shape == oid.shapeuv
    assert oid.wl_d.shape == oid.shapeuv
    assert oid.u.shape == oid.shapeuv
    assert oid.v.shape == oid.shapeuv
    assert oid.pa.shape == oid.shapeuv
    assert oid.bl.shape == oid.shapeuv
    assert oid.blwl.shape == oid.shapeuv
    oid.flatten()
    assert len(oid.shapedata) == 1
    assert len(oid.shapeuv) == 2
    assert oid.shapeuv[-1] == 3
    assert oid.data.shape == oid.shapedata
    assert oid.error.shape == oid.shapedata
    assert oid.wl.shape == oid.shapeuv
    assert oid.wl_d.shape == oid.shapeuv
    assert oid.u.shape == oid.shapeuv
    assert oid.v.shape == oid.shapeuv
    assert oid.pa.shape == oid.shapeuv
    assert oid.bl.shape == oid.shapeuv
    assert oid.blwl.shape == oid.shapeuv

@raises(exc.shapeIssue)
def test_shapeIssue():
    oig = Oigrab(FILENAME_FULL)
    datafilter = oig.filtered(tgt=VALIDTGT)
    oid = Oidata(src=FILENAME_FULL, hduidx=VALIDHDUFAKET3, datatype="T3PHI", hduwlidx=WLHDU, indices=datafilter[VALIDHDUFAKET3])

def test_shapeIssue_noraise():
    oig = Oigrab(FILENAME_FULL)
    datafilter = oig.filtered(tgt=VALIDTGT)
    oid = Oidata(src=FILENAME_FULL, hduidx=VALIDHDUFAKET3, datatype="T3PHI", hduwlidx=WLHDU, indices=datafilter[VALIDHDUFAKET3], raiseError=False)

def test_masking(seed=42):
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    oid = Oidata(src=FILENAME, hduidx=VALIDHDU, datatype="VIS2", hduwlidx=WLHDU, indices=datafilter[VALIDHDU])
    np.random.seed(seed)
    assert not oid._use_mask
    oid.mask = np.random.uniform(low=0.5, high=1.5, size=oid.shapedata).astype(int)
    assert oid._use_mask
    through = oid.mask.sum()
    assert oid.shapedata == (through,)
    assert oid.shapedata == oid.shapeuv
    assert oid.data.shape == oid.shapedata
    assert oid.error.shape == oid.shapedata
    assert oid.wl.shape == oid.shapedata
    assert oid.wl_d.shape == oid.shapedata
    assert oid.u.shape == oid.shapedata
    assert oid.v.shape == oid.shapedata
    assert oid.pa.shape == oid.shapedata
    assert oid.bl.shape == oid.shapedata
    assert oid.blwl.shape == oid.shapedata
    assert np.allclose(oid._data, oid['data'])
    assert np.allclose(oid._error, oid['error'])
    assert np.allclose(oid._wl, oid['wl'])
    assert np.allclose(oid._wl_d, oid['wl_d'])
    assert np.allclose(oid._u, oid['u'])
    assert np.allclose(oid._v, oid['v'])
    assert np.allclose(oid._pa, oid['pa'])
    assert np.allclose(oid._bl, oid['bl'])
    assert np.allclose(oid._blwl, oid['blwl'])
    assert np.allclose(oid['data'][oid.mask], oid.data)
    assert np.allclose(oid['error'][oid.mask], oid.error)
    assert np.allclose(oid['wl'][oid.mask], oid.wl)
    assert np.allclose(oid['wl_d'][oid.mask], oid.wl_d)
    assert np.allclose(oid['u'][oid.mask], oid.u)
    assert np.allclose(oid['v'][oid.mask], oid.v)
    assert np.allclose(oid['pa'][oid.mask], oid.pa)
    assert np.allclose(oid['bl'][oid.mask], oid.bl)
    assert np.allclose(oid['blwl'][oid.mask], oid.blwl)
    for vv in [True, None]:
        oid.mask = vv
        assert not oid._use_mask
        assert oid.shapedata == (4,38)
        assert oid.shapedata == oid.shapeuv
        assert oid.data.shape == oid.shapedata
        assert oid.error.shape == oid.shapedata
        assert oid.wl.shape == oid.shapedata
        assert oid.wl_d.shape == oid.shapedata
        assert oid.u.shape == oid.shapedata
        assert oid.v.shape == oid.shapedata
        assert oid.pa.shape == oid.shapedata
        assert oid.bl.shape == oid.shapedata
        assert oid.blwl.shape == oid.shapedata
    oid.mask = False
    assert oid._use_mask
    assert oid.shapedata == (0,)
    assert oid.shapedata == oid.shapeuv
    assert oid.data.shape == oid.shapedata
    assert oid.error.shape == oid.shapedata
    assert oid.wl.shape == oid.shapedata
    assert oid.wl_d.shape == oid.shapedata
    assert oid.u.shape == oid.shapedata
    assert oid.v.shape == oid.shapedata
    assert oid.pa.shape == oid.shapedata
    assert oid.bl.shape == oid.shapedata
    assert oid.blwl.shape == oid.shapedata

def test_maskingT3(seed=42):
    oig = Oigrab(FILENAME2)
    datafilter = oig.filtered(tgt=VALIDTGT, t3amp=False)
    oid = Oidata(src=FILENAME2, hduidx=VALIDHDUT3, datatype="T3PHI", hduwlidx=WLHDUT3, indices=datafilter[VALIDHDUT3])
    np.random.seed(seed)
    assert not oid._use_mask
    oid.mask = np.random.uniform(low=0.5, high=1.5, size=oid.shapedata).astype(int)
    assert oid._use_mask
    through = oid.mask.sum()
    assert oid.shapedata == (through,)
    assert oid.shapedata +(3,) == oid.shapeuv
    assert oid.data.shape == oid.shapedata
    assert oid.error.shape == oid.shapedata
    assert oid.wl.shape == oid.shapeuv
    assert oid.wl_d.shape == oid.shapeuv
    assert oid.u.shape == oid.shapeuv
    assert oid.v.shape == oid.shapeuv
    assert oid.pa.shape == oid.shapeuv
    assert oid.bl.shape == oid.shapeuv
    assert oid.blwl.shape == oid.shapeuv
    assert np.allclose(oid._data, oid['data'])
    assert np.allclose(oid._error, oid['error'])
    assert np.allclose(oid._wl, oid['wl'])
    assert np.allclose(oid._wl_d, oid['wl_d'])
    assert np.allclose(oid._u, oid['u'])
    assert np.allclose(oid._v, oid['v'])
    assert np.allclose(oid._pa, oid['pa'])
    assert np.allclose(oid._bl, oid['bl'])
    assert np.allclose(oid._blwl, oid['blwl'])
    assert np.allclose(oid['data'][oid.mask], oid.data)
    assert np.allclose(oid['error'][oid.mask], oid.error)
    assert np.allclose(oid['wl'][oid.mask], oid.wl)
    assert np.allclose(oid['wl_d'][oid.mask], oid.wl_d)
    assert np.allclose(oid['u'][oid.mask], oid.u)
    assert np.allclose(oid['v'][oid.mask], oid.v)
    assert np.allclose(oid['pa'][oid.mask], oid.pa)
    assert np.allclose(oid['bl'][oid.mask], oid.bl)
    assert np.allclose(oid['blwl'][oid.mask], oid.blwl)
    for vv in [True, None]:
        oid.mask = vv
        assert not oid._use_mask
        assert oid.shapedata == (140,1)
        assert oid.shapedata +(3,) == oid.shapeuv
        assert oid.data.shape == oid.shapedata
        assert oid.error.shape == oid.shapedata
        assert oid.wl.shape == oid.shapeuv
        assert oid.wl_d.shape == oid.shapeuv
        assert oid.u.shape == oid.shapeuv
        assert oid.v.shape == oid.shapeuv
        assert oid.pa.shape == oid.shapeuv
        assert oid.bl.shape == oid.shapeuv
        assert oid.blwl.shape == oid.shapeuv
    oid.mask = False
    assert oid._use_mask
    assert oid.shapedata == (0,)
    assert oid.shapedata +(3,) == oid.shapeuv
    assert oid.data.shape == oid.shapedata
    assert oid.error.shape == oid.shapedata
    assert oid.wl.shape == oid.shapeuv
    assert oid.wl_d.shape == oid.shapeuv
    assert oid.u.shape == oid.shapeuv
    assert oid.v.shape == oid.shapeuv
    assert oid.pa.shape == oid.shapeuv
    assert oid.bl.shape == oid.shapeuv
    assert oid.blwl.shape == oid.shapeuv

@raises(exc.BadMaskShape)
def test_BadMaskShape():
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    oid = Oidata(src=FILENAME, hduidx=VALIDHDU, datatype="VIS2", hduwlidx=WLHDU, indices=datafilter[VALIDHDU])
    oid.mask = np.array([True, False])

def test_BadMaskShape_noraise():
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    oid = Oidata(src=FILENAME, hduidx=VALIDHDU, datatype="VIS2", hduwlidx=WLHDU, indices=datafilter[VALIDHDU], raiseError=False)
    oid.mask = np.array([True, False])
    assert len(oid.mask.shape) == 2

"""def test_oigrab():
    oig = Oigrab(FILENAME)
    assert len(oig.targets) == 3
    assert oig.targets[0] == 'HD_204770'
    assert str(oig) == repr(oig)"""


@raises(exc.HduDatatypeMismatch)
def test_HduDatatypeMismatch():
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    oid = Oidata(src=FILENAME, hduidx=VALIDHDU, datatype="T3AMP", hduwlidx=WLHDU, indices=datafilter[VALIDHDU])

def test_HduDatatypeMismatch_noraise():
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    oid = Oidata(src=FILENAME, hduidx=VALIDHDU, datatype="T3AMP", hduwlidx=WLHDU, indices=datafilter[VALIDHDU], raiseError=False)

@raises(exc.ReadOnly)
def test_data_readonly():
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    oid = Oidata(src=FILENAME, hduidx=VALIDHDU, datatype="VIS2", hduwlidx=WLHDU, indices=datafilter[VALIDHDU])
    oid.data = 'random'

@raises(exc.ReadOnly)
def test_error_readonly():
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    oid = Oidata(src=FILENAME, hduidx=VALIDHDU, datatype="VIS2", hduwlidx=WLHDU, indices=datafilter[VALIDHDU])
    oid.error = 'random'

@raises(exc.ReadOnly)
def test_u_readonly():
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    oid = Oidata(src=FILENAME, hduidx=VALIDHDU, datatype="VIS2", hduwlidx=WLHDU, indices=datafilter[VALIDHDU])
    oid.u = 'random'

@raises(exc.ReadOnly)
def test_v_readonly():
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    oid = Oidata(src=FILENAME, hduidx=VALIDHDU, datatype="VIS2", hduwlidx=WLHDU, indices=datafilter[VALIDHDU])
    oid.v = 'random'

@raises(exc.ReadOnly)
def test_wl_readonly():
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    oid = Oidata(src=FILENAME, hduidx=VALIDHDU, datatype="VIS2", hduwlidx=WLHDU, indices=datafilter[VALIDHDU])
    oid.wl = 'random'

@raises(exc.ReadOnly)
def test_wl_d_readonly():
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    oid = Oidata(src=FILENAME, hduidx=VALIDHDU, datatype="VIS2", hduwlidx=WLHDU, indices=datafilter[VALIDHDU])
    oid.wl_d = 'random'

@raises(exc.ReadOnly)
def test_bl_readonly():
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    oid = Oidata(src=FILENAME, hduidx=VALIDHDU, datatype="VIS2", hduwlidx=WLHDU, indices=datafilter[VALIDHDU])
    oid.bl = 'random'

@raises(exc.ReadOnly)
def test_paa_readonly():
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    oid = Oidata(src=FILENAME, hduidx=VALIDHDU, datatype="VIS2", hduwlidx=WLHDU, indices=datafilter[VALIDHDU])
    oid.pa = 'random'

@raises(exc.ReadOnly)
def test_blwl_readonly():
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    oid = Oidata(src=FILENAME, hduidx=VALIDHDU, datatype="VIS2", hduwlidx=WLHDU, indices=datafilter[VALIDHDU])
    oid.blwl = 'random'

@raises(exc.ReadOnly)
def test_shapedata_readonly():
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    oid = Oidata(src=FILENAME, hduidx=VALIDHDU, datatype="VIS2", hduwlidx=WLHDU, indices=datafilter[VALIDHDU])
    oid.shapedata = 'random'

@raises(exc.ReadOnly)
def test_shapeuv_readonly():
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    oid = Oidata(src=FILENAME, hduidx=VALIDHDU, datatype="VIS2", hduwlidx=WLHDU, indices=datafilter[VALIDHDU])
    oid.shapeuv = 'random'

@raises(exc.ReadOnly)
def test_is_angle_readonly():
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    oid = Oidata(src=FILENAME, hduidx=VALIDHDU, datatype="VIS2", hduwlidx=WLHDU, indices=datafilter[VALIDHDU])
    oid.is_angle = 'random'

@raises(exc.ReadOnly)
def test_is_t3_readonly():
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    oid = Oidata(src=FILENAME, hduidx=VALIDHDU, datatype="VIS2", hduwlidx=WLHDU, indices=datafilter[VALIDHDU])
    oid.is_t3 = 'random'

@raises(exc.ReadOnly)
def test_flat_readonly():
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    oid = Oidata(src=FILENAME, hduidx=VALIDHDU, datatype="VIS2", hduwlidx=WLHDU, indices=datafilter[VALIDHDU])
    oid.flat = 'random'


def test_data_readonly():
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    oid = Oidata(src=FILENAME, hduidx=VALIDHDU, datatype="VIS2", hduwlidx=WLHDU, indices=datafilter[VALIDHDU], raiseError=False)
    oid.data = 'random'
    assert oid.data is not 'random'

def test_error_readonly():
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    oid = Oidata(src=FILENAME, hduidx=VALIDHDU, datatype="VIS2", hduwlidx=WLHDU, indices=datafilter[VALIDHDU], raiseError=False)
    oid.error = 'random'
    assert oid.error is not 'random'

def test_u_readonly():
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    oid = Oidata(src=FILENAME, hduidx=VALIDHDU, datatype="VIS2", hduwlidx=WLHDU, indices=datafilter[VALIDHDU], raiseError=False)
    oid.u = 'random'
    assert oid.u is not 'random'

def test_v_readonly():
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    oid = Oidata(src=FILENAME, hduidx=VALIDHDU, datatype="VIS2", hduwlidx=WLHDU, indices=datafilter[VALIDHDU], raiseError=False)
    oid.v = 'random'
    assert oid.v is not 'random'

def test_wl_readonly():
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    oid = Oidata(src=FILENAME, hduidx=VALIDHDU, datatype="VIS2", hduwlidx=WLHDU, indices=datafilter[VALIDHDU], raiseError=False)
    oid.wl = 'random'
    assert oid.wl is not 'random'

def test_wl_d_readonly():
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    oid = Oidata(src=FILENAME, hduidx=VALIDHDU, datatype="VIS2", hduwlidx=WLHDU, indices=datafilter[VALIDHDU], raiseError=False)
    oid.wl_d = 'random'
    assert oid.wl_d is not 'random'

def test_bl_readonly():
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    oid = Oidata(src=FILENAME, hduidx=VALIDHDU, datatype="VIS2", hduwlidx=WLHDU, indices=datafilter[VALIDHDU], raiseError=False)
    oid.bl = 'random'
    assert oid.bl is not 'random'

def test_paa_readonly():
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    oid = Oidata(src=FILENAME, hduidx=VALIDHDU, datatype="VIS2", hduwlidx=WLHDU, indices=datafilter[VALIDHDU], raiseError=False)
    oid.pa = 'random'
    assert oid.pa is not 'random'

def test_blwl_readonly():
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    oid = Oidata(src=FILENAME, hduidx=VALIDHDU, datatype="VIS2", hduwlidx=WLHDU, indices=datafilter[VALIDHDU], raiseError=False)
    oid.blwl = 'random'
    assert oid.blwl is not 'random'

def test_shapedata_readonly():
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    oid = Oidata(src=FILENAME, hduidx=VALIDHDU, datatype="VIS2", hduwlidx=WLHDU, indices=datafilter[VALIDHDU], raiseError=False)
    oid.shapedata = 'random'
    assert oid.shapedata is not 'random'

def test_shapeuv_readonly():
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    oid = Oidata(src=FILENAME, hduidx=VALIDHDU, datatype="VIS2", hduwlidx=WLHDU, indices=datafilter[VALIDHDU], raiseError=False)
    oid.shapeuv = 'random'
    assert oid.shapeuv is not 'random'

def test_is_angle_readonly():
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    oid = Oidata(src=FILENAME, hduidx=VALIDHDU, datatype="VIS2", hduwlidx=WLHDU, indices=datafilter[VALIDHDU], raiseError=False)
    oid.is_angle = 'random'
    assert oid.is_angle is not 'random'

def test_is_t3_readonly():
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    oid = Oidata(src=FILENAME, hduidx=VALIDHDU, datatype="VIS2", hduwlidx=WLHDU, indices=datafilter[VALIDHDU], raiseError=False)
    oid.is_t3 = 'random'
    assert oid.is_t3 is not 'random'

def test_flat_readonly():
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    oid = Oidata(src=FILENAME, hduidx=VALIDHDU, datatype="VIS2", hduwlidx=WLHDU, indices=datafilter[VALIDHDU], raiseError=False)
    oid.flat = 'random'
    assert oid.flat is not 'random'

@raises(exc.ZeroErrorbars)
def test_ZeroErrorbars():
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    oid = Oidata(src=FILENAME, hduidx=VALIDHDU, datatype="VIS2", hduwlidx=WLHDU, indices=datafilter[VALIDHDU]-1)

def test_ZeroErrorbars_noraise():
    oig = Oigrab(FILENAME)
    datafilter = oig.filtered(tgt=VALIDTGT)
    oid = Oidata(src=FILENAME, hduidx=VALIDHDU, datatype="VIS2", hduwlidx=WLHDU, indices=datafilter[VALIDHDU]-1, raiseError=False)
    assert not hasattr(oid, "_invvar")
