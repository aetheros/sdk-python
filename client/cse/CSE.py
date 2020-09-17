#!/usr/bin/env python

import json, random

from client.OneM2M.http.OneM2MRequest import OneM2MRequest
from client.OneM2M.OneM2MOperation import OneM2MOperation
from client.exceptions.InvalidArgumentException import InvalidArgumentException
from client.ae.AE import AE

class CSE():
    # Instance of AE returned by register_ae call.
    # ae = None

    RSC = 'PN_CSE'

    def __init__(self, host, port):
        self.transport_protocol = 'http'
        self.host = host
        self.port = port

    def register_ae(self, ae):
        """ Synchronously register an AE with a Policynet CSE.
        
           Args:
            ae: An instance of AE.

           Returns:
            An instanc of AE.

           Raises:
            InvalidArgumentException: If the argument is not an AE.
        """
        if isinstance(ae, AE) is False:
            raise InvalidArgumentException('AE registration expects an instance AE.')

        # Host and resource.
        to = '{}://{}:{}/PN_CSE'.format(self.transport_protocol, self.host, self.port)

        # op is not required as it is implied by the function that the params will be passed to.
        params = {
            'op': 'Create', 
            'to': 'http://{}:{}/{}'.format(self.host, self.port, CSE.RSC),
            'fr': '1234567890',
            'rqi': self._generate_rqi()
        }

        # Create a request object
        oneM2MRequest = OneM2MRequest()

        # Returns a OneM2MResponse object.  Handle any response code logic here.
        oneM2MResponse = oneM2MRequest.create(to, params, ae)

        # Return the AE instance.
        return AE(oneM2MResponse.pc)

    def discover_containers(self, ae):
        """ Synchronously discover containers registered with the MN-CSE.
        
           Args:
            ae: An instance of AE.

           Returns: 
            An instanc of AE containing a list of container URIs.

           Raises:
            InvalidArgumentException: If the argument is not an AE.
        """
        if isinstance(ae, AE) is False:
            raise InvalidArgumentException('Delete AE expects an instance AE.')


        # note: fu (filter usage) parameter required for resource discovery
        to = '{}://{}:{}/{}'.format(self.transport_protocol, self.host, self.port, CSE.RSC)


        # Create a request object
        oneM2MRequest = OneM2MRequest(to)

        oneM2MRequest.set_param(OneM2MRequest.M2M_PARAM_FILTER_USAGE, 1)
        oneM2MRequest.set_param(OneM2MRequest.M2M_PARAM_FROM, ae.ri)
        oneM2MRequest.set_param(OneM2MRequest.M2M_PARAM_REQUEST_IDENTIFIER, self._generate_rqi())
        oneM2MRequest.set_param(OneM2MRequest.M2M_PARAM_RESOURCE_TYPE, '')

        # Returns a OneM2MResponse object.  Handle any response code logic here.
        oneM2MResponse = oneM2MRequest.retrieve()

        pc = json.loads(oneM2MResponse.pc)

        if 'uril' in pc.keys():
            return pc['uril']

        return None

    def create_content_instance(self, ae):
        pass

    def retrieve_resource(self, ae, rsc, rcn=OneM2MRequest.M2M_RCN_ATTRIBUTES_CHILD_RESOURCES):
        """ Synchronous retrieve resource request.
        
           Args:
            rsc: The URI of the resource to retrieve.

           Returns:
            A OneM2MResource object.

           Raises:
            ?
        """

        # Remove leading '/'
        rsc = rsc[1:] if rsc[0] is '/' else rsc

        to = '{}://{}:{}/{}?rcn={}'.format(self.transport_protocol, self.host, self.port, rsc, rcn)

        params = {
            'fr': ae.ri, # resource id.
            'rqi': self._generate_rqi()
        }

        oneM2MRequest = OneM2MRequest(to, params)

        oneM2MReponse = oneM2MRequest.retrieve()

        print(oneM2MReponse.rsc)

        # @todo Return OneM2MResource instance.
        return oneM2MReponse.pc

    def delete_ae(self, ae):
        if isinstance(ae, AE) is False:
            raise InvalidArgumentException('Delete AE expects an instance AE.')
        
        # Host and resource.
        to = '{}://{}:{}/PN_CSE/{}'.format(self.transport_protocol, self.host, self.port, ae.ri)

        # op is not required as it is implied by the function that the params will be passed to.
        params = {
            'op': 'Delete', 
            'to': 'http://{}:{}/PN_CSE/{}'.format(self.host, self.port, ae.ri),
            'fr':  ae.ri,
            'rqi': self._generate_rqi()
        }

        # Create a request object
        oneM2MRequest = OneM2MRequest()

        # Returns a OneM2MResponse object.  Handle any response code logic here.
        oneM2MResponse = oneM2MRequest.delete(to, params)

        # Return the AE instance.
        return oneM2MResponse

    # @todo move to request primitive.
    def _generate_rqi(self):
        return str(random.randrange(1000000,999999999999))
