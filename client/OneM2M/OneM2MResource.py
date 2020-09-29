#!/usr/bin/env python

import json

class OneM2MResource():
    M2M_ATTR_PRIMITIVE_CONTENT = 'pc'

    M2M_TYPE_CONTAINER = '3'

    def __init__(self):
        # Resource short name will be set in derived class constructor.
        self.short_name = None

    def __str__(self):
        return json.dumps(self.__dict__)

    def get_content(self):
        return self.__dict__

# @todo add resouce short name not set exception for OneM2MRequest class to raise.