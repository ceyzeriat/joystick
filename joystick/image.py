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

from . import core
tkinter = core.tkinter
FigureCanvasTkAgg = core.mat.backends.backend_tkagg.FigureCanvasTkAgg
cm = core.mat.cm
np = core.np
time = core.time
from .frame import Frame


__all__ = ['Image']


class Image(Frame):
    def __init__(self, name, freq_up=1, pos=(50, 50), size=(400, 400),
                 screen_relative=False, background="black", foreground='green',
                 cmap='gist_earth', cm_bounds=(None, None), unitperpx=1.,
                 axrect=(0.1, 0.1, 0.9, 0.9), grid=None, **kwargs):
        """
        Initialises an image-frame.

        Args:
          * name (str): the frame name
          * freq_up (float or None): the frequency of update of the frame,
            between 1e-3 and 1e3 Hz, or ``None`` for no update
          * pos (px or %) [optional]: left-top corner position of the
            frame, see ``screen_relative``
          * size (px or %) [optional]: width-height dimension of the
            frame, see ``screen_relative``
          * screen_relative (bool) [optional]: set to ``True`` to give
            ``pos`` and ``size`` as a % of the screen size, or ``False``
            to give then as pixels
          * cmap (colormap name) [optional]: the colormap of the image
          * cm_bounds (tuple of 2 float) [optional]: the (min, max)
            values of the colormap
          * unitperpx (float) [optional]: unit scaling
          * axrect (list of 4 floats) [optional]: the axes bounds (l,b,w,h)
            as in ``plt.figure.add_axes(rect=(l,b,w,h))``
          * grid (color or None) [optional]: the grid color, or no grid
            if ``None``

        Kwargs:
          * aspect: see ``plt.imshow``, default 'auto'
          * origin: see ``plt.imshow``, default 'lower'
          * Any non-abbreviated parameter accepted by ``figure.add_axes``
            and ``plt.imshow``
          * Will be passed to the optional custom methods
        """
        # save input for reinit
        kwargs['name'] = name
        kwargs['freq_up'] = freq_up
        kwargs['pos'] = pos
        kwargs['size'] = size
        kwargs['screen_relative'] = screen_relative
        kwargs['cmap'] = cmap
        kwargs['cm_bounds'] = cm_bounds
        kwargs['unitperpx'] = unitperpx
        kwargs['axrect'] = axrect
        kwargs['grid'] = grid
        self._kwargs = kwargs
        # call mummy init
        super(Image, self).__init__(**self._kwargs)
        # call ya own init
        self._init_base(**self._kwargs)

    def _init_base(self, **kwargs):
        """
        Separate function from __init__ for re-initialization purpose
        """
        before, after = self._extract_callit('init')
        self._callmthd(before, **kwargs)
        self._everset = False
        axrect = tuple(kwargs.pop('axrect')[:4])
        self._fig = core.mat.figure.Figure()
        self.ax = self._fig.add_axes(axrect[:2] + (axrect[2]-axrect[0],
                                                   axrect[3]-axrect[1]),
                                     **core.matkwargs(kwargs))
        self._canvas = FigureCanvasTkAgg(self._fig, master=self._window)
        self._canvas.show()
        self._canvas.get_tk_widget().pack(side=tkinter.TOP,
                                          fill=tkinter.BOTH,
                                          expand=True)
        self._canvas._tkcanvas.pack(side=tkinter.TOP,
                                    fill=tkinter.BOTH,
                                    expand=True)
        grid = kwargs.pop('grid')
        if grid not in [None, False]:
            self.ax.grid(color=grid, lw=1)
        self.reset_image(data=[[0, 0],[0, 0]], **kwargs)
        self._callmthd(after, **kwargs)
        # core.INITMETHOD left for backward compatibility
        if core.INITMETHOD not in after \
            and core.INITMETHOD not in before \
            and hasattr(self, core.INITMETHOD):
            print("DEPRECATION WARNING: You should add the decorator " \
                  "`@_callit('after', 'init')` on `{}`. Refer to example.py" \
                  " ".format(core.INITMETHOD))
            self._callmthd(core.INITMETHOD, **kwargs)

    @property
    def cmap(self):
        """
        The colormap name of the image
        """
        return self._cmap.name

    @cmap.setter
    def cmap(self, value):
        if isinstance(value, str):
            if value in cm.datad.keys():
                self._cmap = cm.get_cmap(value)
        else:
            self._cmap = value
        if self._everset:
            self._img.set_cmap(self._cmap)
    
    @property
    def cm_bounds(self):
        """
        The (min, max) values of the colormap.
        """
        return self._norm.vmin, self._norm.vmax

    @cm_bounds.setter
    def cm_bounds(self, value):
        if self._everset:
            self._set_norm(cm_bounds=value, data=self.get_data())
            self._img.set_norm(self._norm)
        else:
            self._set_norm(cm_bounds=value)

    def _set_norm(self, cm_bounds, data=None):
        """
        Set the plt.Normalize from cm_bounds and optional data
        """
        self._norm = core.cm_bounds_to_norm(cm_bounds=cm_bounds, data=data)

    def reset_image(self, data=None, **kwargs):
        """
        Resets the image in the frame (cmap, cm_bounds), axes, etc,
        using the kwargs provided (default is values of initialization).
        See :py:class:`~joystick.image.Image` for accepted parameters.
        """
        # updates with new reinit value if specified
        for key, v in self._kwargs.items():
            if key not in kwargs.keys():
                kwargs[key] = v
        self.cmap = self._kwargs.get('cmap')
        self._set_norm(cm_bounds=kwargs.get('cm_bounds'), data=data)
        unitperpx = float(kwargs.get('unitperpx'))
        extent = np.asarray(np.shape(data))*unitperpx*0.5
        extent = [-extent[1], extent[1], -extent[0], extent[0]]
        self._img = self.ax.imshow(data, cmap=self._cmap, norm=self._norm,
                                   origin=kwargs.get('origin', 'lower'),
                                   aspect=kwargs.get('aspect', 'auto'),
                                   extent=extent, **core.matkwargs(kwargs))
        self._everset = True

    def reinit(self, **kwargs):
        """
        Re-initializes the frame, i.e. closes the current frame if
        necessary and creates a new one. Uses the parameters of
        initialization by default or anything provided through kwargs.
        See :class:`Image` for the description of input parameters.
        """
        # updates with new reinit value if specified
        self._kwargs.update(kwargs)
        # call mummy reinit
        super(Image, self).reinit(**self._kwargs)
        # ya own reinit
        self._init_base(**self._kwargs)

    def show(self):
        """
        Updates the image
        """
        if self.visible:
            self._canvas.draw()

    def set_data(self, data):
        """
        Sets the image. If the data shape does not corerspond to the
        current data shape, the :py:func:`~joystick.image.Image.reset_image` is called.
        """
        if self.visible:
            old_data = self.get_data()
            if not self._everset or old_data.shape != data.shape:
                self.reset_image(data=data)
            else:
                if not np.allclose(old_data, data):
                    self._img.set_data(data)

    def get_data(self):
        """
        Returns the image.
        """
        if self.visible and self._everset:
            return self._img.get_array().data
