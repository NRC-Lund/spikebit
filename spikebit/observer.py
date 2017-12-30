#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: bengt
"""
import weakref
DATA_RECEIVED = 1


class Observable(object):
    """ Observable super class
    """
    
    def __init__(self):
        self._observers = weakref.WeakSet()

    def register_observer(self, observer):
        """ Register an observer of the observable

        args:
            observer: Observer to be registered
        """
        self._observers.add(observer)

    def notify_observers(self, msg):
        """ Notify observers of change in observable

        args:
            msg: message received; one of the constants in this class
        """
        for observer in self._observers:
            observer.notify(self, msg)


class Observer(object):
    """
    Observer super class
    """
    def __init__(self):
        pass

    def start_observing(self, subject):
        subject.register_observer(self)

    def notify(self, subject, msg):
        pass
