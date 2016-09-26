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

from threading import Thread
import time
from functools import wraps

from . import core

__all__ = ['deco_infinite_loop']

def deco_infinite_loop(wait_time=0.5):
    """
    This decorator creates a daemon-thread to call a decotared
    joystick method in an infinite loop every wait_time seconds, as
    long as the joystick.running attribute is True, or until the end
    of the universe, whichever is first.
    
    This is a self-aware decorator, recording all function names
    decorated with itself, such that all threads can be launched
    simultaneously with the joystick.start() method.

    However, it must be initialized at run-time before use:
    > class yuhu(joystick.Joystick):
    >     _infinite_loop = joystick.deco_infinite_loop()
    >     ...
    (the reason is that it must get a memory copy of the decorator
     function in order to record the decorated functions in the
     desired scope, not in the pakage import scope.
     In short, just initilize it as above and it will work)

    It then can be used normally:
    > @_infinite_loop(wait_time=0.5)  # in sec
    > def repetitive_task():
    >     print("Next time I'm done I swear.")
    """
    # just a layer to get a memory copy of the decorator at run-time
    def infinite_loop_static(wait_time=wait_time):  # in sec
        # the top-level decorator, with defaulted wait_time
        def func_decorator(func):
            # the actual decorator
            @wraps(func)
            def func_wrapper(self):
                # the wrapper, to get pretty docstrings
                def fct(self):
                    # the looping function
                    while self.running:  # cf joystick class
                        func(self)  # finally calling some stuff
                        if wait_time not in [None, False]:
                            time.sleep(wait_time)
                # register the Thread and start it
                loopy = Thread(target=fct, args=(self,))
                loopy.daemon = True
                loopy.start()
            # at class-definition, this adds the function name in the
            # top-level decorator
            core.append(infinite_loop_static, 'fcts', func.func_name)
            return func_wrapper
        return func_decorator
    return infinite_loop_static
