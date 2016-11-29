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
    # initialize the infinite loop and callit decorators so they can auto-
    # register methods they decorate
    _infinite_loop = jk.deco_infinite_loop()
    _callit = jk.deco_callit()

    @_callit('before', 'init')
    def _init_data(self, *args, **kwargs):
        # Function automatically called at initialization, thanks to the
        # decorator
        self.xdata = np.array([])  # time x-axis
        self.ydata1 = np.array([])  # fake data y-axis
        self.ydata2 = np.array([])  # fake data y-axis

    @_callit('after', 'init')
    def _build_frames(self, *args, **kwargs):
        # Function automatically called at initialization, thanks to the
        # decorator. It will be called after "_init_data" given that it is
        # declared after
        # create a graph frame
        self.mygraph = self.add_frame(
                    jk.GraphMulti(name="test", size=(500, 500), pos=(50, 50),
                                  xnpts=15, freq_up=7, bgcol="w", nlines=2,
                                  xlabel='t', ylabel='rnd'))
        # create a text frame
        self.mytext = self.add_frame(
                    jk.Text(name="Y-overflow", size=(500, 250), pos=(600, 50),
                            freq_up=1))
        self.myscatter = self.add_frame(
                    jk.Scatter(name="scatter", size=(500, 500), pos=(600, 350),
                               xnpts=15, freq_up=7, bgcol="k", cmap='Reds',
                               s=80, xylim=(0,10,0,1), grid='w'))

    @_callit('before', 'start')
    def _set_t0(self):
        # initialize t0 at start-up
        self._t0 = time.time()

    @_infinite_loop(wait_time=0.2)
    def _get_data(self):
        # This method will automatically be called with simulation start
        # (t.start()), and looped every 0.2 sec in a separate thread as long as
        # the simulation runs (running == True)
        # It gets new data (fake random data) and pushes it to the frames.
        # concatenate data on the time x-axis
        new_x_data = time.time()
        self.xdata = jk.add_datapoint(self.xdata,
                                      new_x_data,
                                      xnptsmax=self.mygraph.xnptsmax)
        # concatenate data on the fake data y-axis
        new_y_data = np.random.random()*1.05
        # check overflow for the new data point
        if new_y_data > 1:
            # send warning to the text-frame
            self.mytext.add_text('Some data bumped into the ceiling: '
                                 '{:.3f}'.format(new_y_data))
        self.ydata1 = jk.add_datapoint(self.ydata1,
                                       new_y_data,
                                       xnptsmax=self.mygraph.xnptsmax)
        # prepare the time axis
        t = np.round(self.xdata-self._t0, 1)
        # push new data to the graph
        self.mygraph.set_xydata([t, t], [self.ydata1, 1-self.ydata1**2])
        self.myscatter.set_xydata(self.ydata1, self.ydata1**2, c=self.ydata1)

    @_callit('before', 'exit')
    def exit_warning(self):
        # Just a warning, automatically called with the exit method, and
        # before the exiting actually takes place (closing frames, etc)
        print("You're about to exit, frames will disappear in 1 second")
        time.sleep(1)

t = test()
t.start()

t.mygraph.xylim = (None, None, 0, 1)

t.mygraph.xnpts = 50

t.mygraph.freq_up = 2
t.myscatter.xylim = (0,1,0,1)

t.mygraph.numbering = False
t.mygraph.lbls = ['rnd', 'rnd**2']

t.myscatter.cmap = 'gist_earth'

t.stop()

t.mygraph.reinit(bgcol='w', axrect=(0,0,1,1), xylim=(None, None, 0, 1))

t.start()

t.stop()

t.exit()
