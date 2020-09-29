#!/usr/bin/env python

import json

from client.OneM2M.OneM2MResource import OneM2MResource

# TS-0001 9.6.5 Resource Type AE.
class AE(OneM2MResource):
    # AE specific resource attibutes
    # TS-0004 Table 8.2.3-1
    # @todo add remaining AE specific attributes.
    M2M_ATTR_APP_ID = 'api'
    M2M_ATTR_AE_ID = 'aei'
    M2M_ATTR_APP_NAME = 'apn'
    M2M_ATTR_POINT_OF_ACCESS = 'poa'

    # Attributes that must be defined in each instance.
    REQUIRED_ATTRIBUTES = [
        M2M_ATTR_AE_ID
    ]
    
    def __init__(self, args):
        """Constructor
            Expects a dictionary representation of an AE to generate members.
        """

        # Resource short name.
        OneM2MResource.short_name = 'ae'

        # Expects a dict, but should handle the string representation of a json object.
        # Clearer when deserializing response content to an object.
        if isinstance(args, str):
            args = json.loads(args)

        # CSE returns a resource wrapped in a containing json object with the resource
        # name as its key ex. {"ae": {"aei": "", ...}}.  For AE instantiation and deserialization
        # check for an ae member.  If a regular instantiation using an initialization dict, ignore.
        if 'ae' in tuple(args.keys()):
            ae = args['ae']
        else:
            ae = args

        self._validate_attributes(ae)
        self.__dict__ = ae

    def __str__(self):
        """Print string repr when print is called on object.
        """
        return json.dumps(self.__dict__)

    def __repr__(self):
        """Print string when repr is called on object.
        """
        return json.dumps(self.__dict__)
        
    def _validate_attributes(self, ae):
        """ Validates attribute.
        """
        ae_attributes = list(ae.keys())

        for req_attr in self.REQUIRED_ATTRIBUTES:
            if req_attr not in ae_attributes:
                raise MissingRequiredAttibuteError('Missing required attribute in AE: "{}"'.format(req_attr))

class MissingRequiredAttibuteError(Exception):
    """
    """
    def __init__(self, msg):
        self.message = msg