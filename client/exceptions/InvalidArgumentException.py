#!/usr/bin/env python

from .BaseException import BaseException

class InvalidArgumentException(BaseException):
    def __init__(self, msg):
        self.message = msg