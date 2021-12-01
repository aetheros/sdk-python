# Copyright (c) Aetheros, Inc.  See COPYRIGHT

#!/usr/bin/env python

import json

from typing import Dict, Any

OneM2MResourceContent = Dict[str, Any]

class OneM2MResource:

    M2M_ATTR_PRIMITIVE_CONTENT = 'pc'

    M2M_TYPE_CONTAINER = '3'

    ri = None

    def __init__(self, short_name: str, dict: OneM2MResourceContent = None):
        # Resource short name will be set in derived class constructor.
        if dict is not None:
            self.__dict__ = dict
        self.short_name = short_name

    def __str__(self):
        return json.dumps(self.__dict__)

    def get_content(self):
        return {i:self.__dict__[i] for i in self.__dict__ if i != 'short_name'}


# @todo add resouce short name not set exception for OneM2MRequest class to raise.