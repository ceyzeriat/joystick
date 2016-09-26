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
In short, this framework can replace a Graphical User Interface (GUI) on many projects, as long as 1) the user is confortable enough with console command-line controlling, and 2) the real-time data is not too complex to display).

Allright - let's talk clearly. You have some data-stream (serial port, web scraping, on-going simulation, etc), and you would like to plot in real-time whatever is happening on this stream, and not only that, you would also like to send commands to the thread producing or gathering the data without having to build a full GUI-control.

This package is specifically designed for you.

Joystick is based on Tkinter to display frames of text or graph.


It is released under the GNU General Public License v3 or later (GPLv3+).

.. code-block:: python

    import joystick as jk

    o=obs.Observation('vlt', local_date=(2015, 1, 1), moonAvoidRadius=15, horizon_obs = 40)
    o.add_target('aldebaran')
    o.add_target('canopus')
    o.plot()

#.. image:: https://raw.githubusercontent.com/ceyzeriat/joystick/master/img/obs_ex.png
#   :align: center

.. code-block:: python

    aldebaran = o.targets[0]
    aldebaran.whenobs(o, (2015,1,1), (2015, 2, 1))

#.. image:: https://raw.githubusercontent.com/ceyzeriat/joystick/master/img/aldebaran_when.png
#   :align: center

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
