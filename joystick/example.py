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


import joystick as jk
import numpy as np
import time


class test(jk.Joystick):
    # initialize the infinite loop and callit decorators
    _infinite_loop = jk.deco_infinite_loop()
    _callit = jk.deco_callit()

    @_callit('before', 'init')
    def _init_data(self, *args, **kwargs):
        """
        Function called (first) at initialization, thanks to the decorator
        """
        self._t0 = time.time()  # initialize time
        self.xdata = np.array([self._t0])  # time x-axis
        self.ydata = np.array([0.0])  # fake data y-axis

    @_callit('after', 'init')
    def _build_frames(self, *args, **kwargs):
        """
        Function called (second) at initialization, thanks to the decorator
        """
        # create a graph frame
        self.mygraph = self.add_frame(
                       jk.Graph(name="test", size=(500, 500), pos=(50, 50),
                                fmt="go-", xnpts=15, freq_up=7, bgcol="y",
                                xylim=(0,10,0,1)))
        # create a text frame
        self.mytext = self.add_frame(
                      jk.Text(name="Y-overflow", size=(500, 250),
                              pos=(600, 50), freq_up=2))
        # create an image frame
        self.myimg = self.add_frame(
                      jk.Image(name="IMG", size=(0.1, 0.1), pos=(0.3, 0.3),
                               screen_relative=True, axrect=(0,0,1,1),
                               freq_up=3, cm_bounds = (0, 1)))
    
    @_callit('before', 'exit')
    def exit_warning(self):
        print("OMG, you're about to exit")

    @_infinite_loop(wait_time=0.2)
    def _generate_fake_data(self):  # function looped every 0.2 second
        """
        Loop starting with simulation start, getting data and
        pushing it to the graph every 0.2 seconds
        """
        # concatenate data on the time x-axis
        self.xdata = jk.core.add_datapoint(self.xdata,
                                           time.time(),
                                           xnptsmax=self.mygraph.xnptsmax)
        # concatenate data on the fake data y-axis
        self.ydata = jk.core.add_datapoint(self.ydata,
                                           np.random.random()*1.05,
                                           xnptsmax=self.mygraph.xnptsmax)
        # check overflow for the last data point added
        if self.ydata[-1] > 1:
            # send warning to the text-frame
            self.mytext.add_text('Some data bumped into the ceiling: '
                                 '{:.3f}'.format(self.ydata[-1]))
        # prepare the time axis
        t = np.round(self.xdata-self._t0, 1)
        # push new data to the graph
        self.mygraph.set_xydata(t, self.ydata)

    @_infinite_loop(wait_time=5)
    def _generate_fake_image(self):  # function looped every 5 second
        data = np.random.random((10,10))**3
        self.myimg.set_data(data)
        self.mytext.add_text('Updated graph, mean: {:.3f}'.format(data.mean()))

t = test()
t.start()

t.mygraph.xylim = (None, None, 0, 1)

t.mygraph.xnpts = 50

t.mygraph.freq_up = 2

t.stop()

t.mygraph.reinit(bgcol='w', axrect=(0,0,1,1), xylim=(None, None, 0, 1))

t.start()

t.stop()

t.exit()
