#!/usr/bin/env python

import json

from client.OneM2M.http.OneM2MRequest import OneM2MRequest
from client.OneM2M.OneM2MOperation import OneM2MOperation
from client.exceptions.InvalidArgumentException import InvalidArgumentException
from client.ae.AE import AE

class CSE():
    # Instance of AE returned by register_ae call.
    # ae = None

    def __init__(self, host, port):
        self.https = False
        self.host = host
        self.port = port

    def register_ae(self, ae):
        """Register the AE with the CSE.
        """
        if isinstance(ae, AE) is False:
            raise InvalidArgumentException('AE registration expects an instance AE.')

        # Use https?
        transport_protocol = 'https' if self.https else 'http'

        # Host and resource.
        to = '{}://{}:{}/PN_CSE'.format(transport_protocol, self.host, self.port)

        # op is not required as it is implied by the function that the params will be passed to.
        params = {
            # 'op': 'Create', 
            'to': 'http://{}:{}/PN_CSE'.format(self.host, self.port),
            'fr': '1234567890',
            'rqi': '0987654324321'
        }

        # Create a request object
        oneM2MRequest = OneM2MRequest()

        # Returns a OneM2MResponse object.
        oneM2MResponse = oneM2MRequest.create(to, params, ae)

        # Create an instance of AE from the response content (pc).
        return AE(oneM2MResponse.pc)

