#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Implementation of client observer   
@author: bengt
"""
import weakref
DATA_RECEIVED = 1


class Observable(object):
    def __init__(self):
        self._observers = weakref.WeakSet()

    def register_observer(self, observer):
        self._observers.add(observer)

    def notify_observers(self, msg):
        for observer in self._observers:
            observer.notify(self, msg)


class Observer(object):
    def __init__(self):
        pass

    def start_observing(self, subject):
        subject.register_observer(self)

    def notify(self, subject, msg):
        pass
