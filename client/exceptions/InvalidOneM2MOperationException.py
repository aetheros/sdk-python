#!/usr/bin/env python

from .BaseException import BaseException

class InvalidOneM2MOperationException(BaseException):
    def __init__(self, msg):
        self.message = msg