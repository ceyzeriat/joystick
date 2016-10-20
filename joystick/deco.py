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

__all__ = ['deco_infinite_loop', 'deco_thread_it', 'deco_callit']

POSSIBLE_METH = ['init', 'start', 'stop', 'exit', 'add_frame']

def deco_infinite_loop(wait_time=0.5):
    """
    This decorator creates a daemon-thread to call the decotared
    joystick method in an infinite loop every `wait_time` seconds, as
    long as the joystick.running attribute is True, or until the end
    of the universe, whichever is first.
    
    This is a self-aware decorator, recording all function names
    decorated with itself, such that all threads can be launched
    simultaneously with the joystick.start() method.

    However, it must be initialized at run-time before use:

    >>> class yuhu(joystick.Joystick):
    >>>     _infinite_loop = joystick.deco_infinite_loop()
    >>>     ...
    
    (the reason is that it must get a memory copy of the decorator
     function in order to record the decorated functions in the
     desired scope, not in the pakage import scope.
     In short, just initilize it as above and it will work)

    It then can be used normally:

    >>> @_infinite_loop(wait_time=0.5)  # in sec
    >>> def repetitive_task(self, ...):
    >>>     print("Next time I'm done I swear.")
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
            core.append(infinite_loop_static, 'fcts', getattr(func, 'func_name', getattr(func, '__name__', None)))
            return func_wrapper
        return func_decorator
    return infinite_loop_static


def deco_thread_it(func):
    """
    This decorator creates a daemon-thread to wrap the decotared
    function into a separate thread that is started at the call
    of the function (not with simulation start)

    >>> @joystick.deco_thread_it
    >>> def wait_and_print(txt, wait_time=0.5):
    >>>     time.sleep(wait_time)
    >>>     print("Hey, btw: {}".format(txt))
    """
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        # the wrapper, to get pretty docstrings
        # register the Thread and start it
        loopy = Thread(target=func, args=args, kwargs=kwargs)
        loopy.daemon = True
        loopy.start()
    return func_wrapper


def deco_callit(when='after', fct="init"):
    """
    This decorator, when applied to a function `f`, registers it as to
    called before the joystick method given as input parameter, e.g.
    `init`.
    
    This is a self-aware decorator, recording all function names
    decorated with itself, such that all threads can be launched
    simultaneously with the joystick.start() method.

    However, it must be initialized at run-time before use:

    >>> class yuhu(joystick.Joystick):
    >>>     _callit = joystick.deco_callit()
    >>>     ...
    
    (the reason is that it must get a memory copy of the decorator
     function in order to record the decorated functions in the
     desired scope, not in the pakage import scope.
     In short, just initilize it as above and it will work)

    It then can be used normally:

    >>> @_callit('before', 'exit')
    >>> def call_before_exit(txt):
    >>>     print("OMG, you're about to exit")
    """
    # just a layer to get a memory copy of the decorator at run-time
    def deco_callit_static(when=when, fct=fct):
        # the top-level decorator, with defaulted fct
        fct = fct.lower()
        if fct not in POSSIBLE_METH:
            raise ValueError("'fct' parameter shall be in {}".format(POSSIBLE_METH))
        after = str(when).lower()[0] == 'a'
        def func_decorator(func):
            # the actual decorator
            @wraps(func)
            def func_wrapper(self, **kwargs):
                # the wrapper, to get pretty docstrings
                func(self, **kwargs)  # finally calling some stuff
            # at class-definition, this adds the function name in the
            # top-level decorator
            core.append(deco_callit_static, ("after" if after else "before") + "_" + fct, getattr(func, 'func_name', getattr(func, '__name__', None)))
            return func_wrapper
        return func_decorator
    return deco_callit_static
