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



class test(jk.Joystick):
    # initialize the infinite loop ninja-decorator
    _infinite_loop = jk.deco_infinite_loop(wait_time=2.5)  # set default wait

    def _init(self, *args, **kwargs):
        self._t0 = jk.core.timestamp()
        self.xdata = np.array([self._t0])
        self.ydata = np.array([0.0])
        self.zdata = np.array([0.0])
        self.graph1 = jk.Graph(daddy=self, name="blah1", size=(500, 500), pos=(50, 50), fmt="go-", xnpts=15, freq_up=7, bgcol="y")
        self.text1 = jk.Text(daddy=self, name="blah1", size=(500, 250), pos=(600, 50), freq_up=1.5)

    @_infinite_loop(wait_time=0.2)
    def _generate_fake_data(self):
        """
        The global function that gets all data
        """
        self.xdata = jk.core.add_datapoint(self.xdata, jk.core.timestamp())
        self.ydata = jk.core.add_datapoint(self.ydata, np.random.random()*1.1)
        self.zdata = jk.core.add_datapoint(self.zdata, np.random.random()*1.1)

    @_infinite_loop(wait_time=0.2)
    def _push_data(self):
        t = np.round(self.xdata-self._t0, 1)
        self.graph1.set_xydata(t, self.ydata)
        self.text1.add_text('Added pts at {}'.format(t[-1]))
