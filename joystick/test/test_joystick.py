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


import numpy as np
import time

from ..joystick import Joystick
from ..deco import deco_infinite_loop, deco_callit
from ..graph import Graph
from ..image import Image
from ..text import Text
from ..graphmulti import GraphMulti
from ..scatter import Scatter
from .. import core


# VERY IMPORTANT - screen_relative must be False for testing (not supported by
#   Travis)


def _generate_fake_data_base(self):
    self.xdata = core.add_datapoint(self.xdata,
                                    time.time(),
                                    xnptsmax=self.mygraph.xnptsmax)
    # concatenate data on the fake data y-axis
    self.ydata1 = core.add_datapoint(self.ydata1,
                                    np.random.random()*1.05,
                                    xnptsmax=self.mygraph.xnptsmax)
    # check overflow for the last data point added
    if self.ydata1[-1] > 1:
        # send warning to the text-frame
        self.mytext.add_text('Some data bumped into the ceiling: ' \
                             '{:.3f}'.format(self.ydata1[-1]))
    # prepare the time axis
    t = np.round(self.xdata-self._t0, 1)
    # push new data to the graph
    self.mygraph.set_xydata(t, self.ydata1)
    self.mmgraph.set_xydata([t, t], [self.ydata1, self.ydata2])
    self.myscat.set_xydata(self.ydata1, self.ydata1**2, c=self.ydata1)


def _generate_fake_image_base(self):
    data = np.random.random((10,10))**3
    self.myimg.set_data(data)
    self.mytext.add_text('Updated graph, mean: {:.3f}'.format(data.mean()))


def _build_frames_base(self):
    self.mmgraph = self.add_frame(
                GraphMulti(name="GraphMulti", size=(500, 500), pos=(50, 50),
                           xnpts=15, freq_up=7, bgcol="y", nlines=2,
                           xylim=(0,10,0,1), xlabel='t', ylabel='rnd'))
    self.mytext = self.add_frame(
                    Text(name="Text", size=(500, 250),
                         pos=(600, 50), freq_up=1))
    self.mygraph = self.add_frame(
                    Graph(name="Graph", size=(500, 500),
                          pos=(50, 50), fmt="go-", xnpts=15,
                          freq_up=7, bgcol="y", xylim=(0,10,0,1)))
    self.myimg = self.add_frame(
                    Image(name="Image", size=(100, 100), pos=(50, 600),
                          axrect=(0,0,1,1), freq_up=3,
                          cm_bounds = (0, 1)))
    self.myscat = self.add_frame(
                    Scatter(name="scatter", size=(500, 500), pos=(600, 350),
                               xnpts=15, freq_up=7, bgcol="k", cmap='Reds',
                               s=80, xylim=(0,10,0,1), grid='w'))


class test(Joystick):
    _infinite_loop = deco_infinite_loop()

    def _init(self, *args, **kwargs):
        self._t0 = time.time()
        self.xdata = np.array([])
        self.ydata1 = np.array([])
        self.ydata2 = np.array([])
        _build_frames_base(self)        

    @_infinite_loop(wait_time=1)
    def _generate_fake_data(self):
        _generate_fake_data_base(self)

    @_infinite_loop(wait_time=5)
    def _generate_fake_image(self):
        _generate_fake_image_base(self)


class test2(Joystick):
    _infinite_loop = deco_infinite_loop()
    _callit = deco_callit()

    @_callit('before', 'init')
    def _init_data(self, *args, **kwargs):
        self.xdata = np.array([])
        self.ydata1 = np.array([])
        self.ydata2 = np.array([])

    @_callit('after', 'init')
    def _build_frames(self, *args, **kwargs):
        _build_frames_base(self)

    @_callit('before', 'start')
    def _set_t0(self):
        self._t0 = time.time()

    @_infinite_loop(wait_time=1)
    def _generate_fake_data(self):
        _generate_fake_data_base(self)

    @_infinite_loop(wait_time=5)
    def _generate_fake_image(self):
        _generate_fake_image_base(self)


def _hophop():
    t = test()
    t.start()
    time.sleep(1)
    t.mygraph.xylim = (None, None, 0, 1)
    t.mygraph.xnpts = 50
    t.mygraph.freq_up = 2
    time.sleep(1)
    t.stop()
    t.mygraph.reinit(bgcol='w', axrect=(0,0,1,1), xylim=(None, None, 0, 1))
    time.sleep(1)
    t.start()
    time.sleep(1)
    t.mmgraph.lbls = None
    t.mmgraph.lbls = ['aa', 'bb']
    t.mmgraph.legend(show=True, lbls=None)
    t.mmgraph.legend(show=False)
    t.mmgraph.numbering = True
    t.mmgraph.numbering = False
    t.myscat.vmin = None
    t.myscat.vmax = None
    t.myscat.cmap = 'jet'

    t.stop()
    t.exit()

def _hophophop():
    t = test()
    time.sleep(1)
    t.exit()


def testdeprecated_create():
    _hophophop()

def testdeprecated_play():
    _hophop()

def test_create():
    _hophophop()

def test_play():
    _hophop()
