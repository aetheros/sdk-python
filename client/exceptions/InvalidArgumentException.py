# Copyright (c) Aetheros, Inc.  See COPYRIGHT

#!/usr/bin/env python

from .BaseException import BaseException


class InvalidArgumentException(BaseException):
    def __init__(self, msg: str):
        self.message = msg