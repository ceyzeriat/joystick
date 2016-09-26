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
from ..deco import deco_infinite_loop
from ..graph import Graph
from ..text import Text
from .. import core

class test(Joystick):
   # initialize the infinite loop decorator
    _infinite_loop = deco_infinite_loop()

    def _init(self, *args, **kwargs):
        """
        Function called at initialization, don't bother why for now
        """
        self._t0 = time.time()  # initialize time
        self.xdata = np.array([self._t0])  # time x-axis
        self.ydata = np.array([0.0])  # fake data y-axis
        # create a graph frame
        self.mygraph = Graph(daddy=self, name="test", size=(500, 500),
                                pos=(50, 50), fmt="go-", xnpts=15,
                                freq_up=7, bgcol="y", xylim=(0,10,0,1))
        # create a text frame
        self.mytext = Text(daddy=self, name="Y-overflow",
                              size=(500, 250), pos=(600, 50), freq_up=1)

    @_infinite_loop(wait_time=0.2)
    def _generate_fake_data(self):  # function looped every 0.2 second
        """
        Loop starting with simulation start, getting data and
        pushing it to the graph every 0.2 seconds
        """
        # concatenate data on the time x-axis
        self.xdata = core.add_datapoint(self.xdata,
                                           time.time())
        # concatenate data on the fake data y-axis
        self.ydata = core.add_datapoint(self.ydata,
                                           np.random.random()*1.05)
        # check overflow for the last data point added
        if self.ydata[-1] > 1:
            # send warning to the text-frame
            self.mytext.add_text('Some data bumped into the ceiling: '
                                 '{:.3f}'.format(self.ydata[-1]))
        # prepare the time axis
        t = np.round(self.xdata-self._t0, 1)
        # push new data to the graph
        self.mygraph.set_xydata(t, self.ydata)


def test_joystick():
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
    t.stop()
    t.exit()
