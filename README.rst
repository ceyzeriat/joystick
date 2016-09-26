.. joystick
===========

.. image:: http://img.shields.io/travis/ceyzeriat/joystick/master.svg?style=flat
    :target: https://travis-ci.org/ceyzeriat/joystick
.. image:: https://coveralls.io/repos/github/ceyzeriat/joystick/badge.svg?branch=master
    :target: https://coveralls.io/github/ceyzeriat/joystick?branch=master
.. image:: http://img.shields.io/badge/license-GPLv3-blue.svg?style=flat
    :target: https://github.com/ceyzeriat/joystick/blob/master/LICENSE

:Name: joystick
:Website: https://github.com/ceyzeriat/joystick
:Author: Guillaume Schworer
:Version: 0.1

Joystick provides a light-weight and simple framework to real-time plotting and logging data while the console remains accessible to control the on-going simulation and/or data acquisition.

In short, this framework can replace a Graphical User Interface (GUI) on many projects, as long as 1) the user is confortable enough with console command-line controlling, and 2) the real-time data is not too complex to display.

Allright - let's talk clearly. You have some data-stream (serial port, web scraping, on-going simulation, etc), and you would like to plot or log in real-time whatever is happening on this stream. Not only that, in additing you would also like to send commands to the thread producing or gathering the data to control the data-stream mechanisms... without having to build a GUI (which looks pretty to your boss, but is time-consumming both in initial design and maintenance).

Then, this package is for you.

Note that Joystick is based on Tkinter to display frames of text or graph, and that it is released under the GNU General Public License v3 or later (GPLv3+).


Straight to the point: check-out this example. It generates fake random data (ydata) between 0 and 1.05 every 0.2 second, which is displayed in a graph as a function of time. Whenever there is a datapoint above 1, it drops a warning in the text-frame.

.. code-block:: python

    import joystick as jk
    import numpy as np
    import time

    class test(jk.Joystick):
        _infinite_loop = jk.deco_infinite_loop()

        def _init(self, *args, **kwargs):
            """
            Function called at initialization, don't bother why for now
            """
            self._t0 = time.time()
            self.xdata = np.array([self._t0])
            self.ydata = np.array([0.0])
            self.mygraph = jk.Graph(daddy=self, name="test", size=(500, 500),
                                    pos=(50, 50), fmt="go-", xnpts=15,
                                    freq_up=7, bgcol="y")
            self.mytext = jk.Text(daddy=self, name="Y-overflow",
                                  size=(500, 250), pos=(600, 50), freq_up=1)

        @_infinite_loop(wait_time=0.2)
        def _generate_fake_data(self):
            """
            Function called at simulation start, getting data and
            pushing it to the graph every 0.2 seconds
            """
            self.xdata = jk.core.add_datapoint(self.xdata,
                                               time.time())
            self.ydata = jk.core.add_datapoint(self.ydata,
                                               np.random.random()*1.05)
            if self.ydata[-1] > 1:
                self.mytext.add_text('Some data bumped into the ceiling: '
                                     '{:.3f}'.format(self.ydata[-1]))
            t = np.round(self.xdata-self._t0, 1)
            self.mygraph.set_xydata(t, self.ydata)

    t = test()
    t.start()

Now you should see a 'snake' going through the frame, but after 10 seconds, it is gone. Type (line by line):

.. code-block:: python

    t.mygraph.xylim = (None, None, 0, 1)
    t.mygraph.xnpts = 50
    t.mygraph.freq_up = 2

Now that should be better, displaying the latest 50 points, at a slower pace (twice a second). Let's stop and reinitialize the graph:

.. code-block:: python

    t.stop()
    t.mygraph.reinit(bgcol='w', axrect=(0,0,1,1), fmt='ko:', xylim=(None, None, 0, 1))
    t.start()
    t.stop()

Here is what it should look like:

.. image:: https://raw.githubusercontent.com/ceyzeriat/joystick/master/docs/img/view.jpg
   :align: center


Documentation
=============

Refer to this page, http://pythonhosted.org/joystick/joystick.html


Requirements
============

joystick requires the following Python packages:

* NumPy: for basic numerical routines
* matplotlib: for plotting


Installation
============

The easiest and fastest way for you to get the package and run is to install joystick through pip::

  $ pip install joystick

You can also download joystick source from GitHub and type::

  $ python setup.py install

Dependencies will not be installed automatically. Refer to the requirements section. If you have an anaconda distribution, you will be good to go.

Contributing
============

Code writing
------------

Code contributions are welcome! Just send a pull request on GitHub and we will discuss it. In the `issue tracker`_ you may find pending tasks.

Bug reporting
-------------

If you think you've found one please refer to the `issue tracker`_ on GitHub.

.. _`issue tracker`: https://github.com/ceyzeriat/joystick/issues

Additional options
------------------

You can either send me an e-mail or add it to the issues/wishes list on GitHub.

Citing
======

If you use joystick on your project, please
`drop me a line <mailto:{my first name}.{my family name}@gmail.com>`, you will get fixes and additional options earlier.

License
=======

joystick is released under the GNU General Public License v3 or later (GPLv3+). Please refer to the LICENSE file.
