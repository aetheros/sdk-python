# Copyright (c) Aetheros, Inc.  See COPYRIGHT

#!/usr/bin/env python

import json, random

from client.ae.AE import AE
from client.onem2m.OneM2MResource import OneM2MResource, OneM2MResourceContent
from client.onem2m.OneM2MPrimitive import OneM2MPrimitive
from client.onem2m.http.OneM2MRequest import OneM2MRequest
from client.onem2m.OneM2MOperation import OneM2MOperation
from client.onem2m.resource.ContentInstance import ContentInstance as ContentInstance
from client.onem2m.resource.Subscription import Subscription
from client.exceptions.InvalidArgumentException import InvalidArgumentException

from typing import List, Optional

class CSE:


    CSE_RESOURCE = 'PN_CSE'

    ae: Optional[AE] = None
    def __init__(self, host: str, port: int, rsc: str = None, transport_protocol = 'http'):
        """Constructor

        Args:
            host (str): CSE host
            port (int): CSE port
            rsc (str): Base resource
        """
        self.transport_protocol = transport_protocol
        self.host = host
        self.port = port
        self.rsc = rsc or CSE.CSE_RESOURCE

    def register_ae(self, ae: AE):
        """Synchronously register an AE with a CSE.

        Args:
            ae (AE): The AE to register.

        Returns:
            OneM2MResponse: The request response.

        Raises:
            InvalidArgumentException: If the argument is not an AE or a dict containing AE attributes.
        """
        if isinstance(ae, AE) is False:
            raise InvalidArgumentException('AE registration expects an instance AE.')

        # Host and resource.
        to = '{}://{}:{}/PN_CSE'.format(self.transport_protocol, self.host, self.port)

        # op is not required as it is implied by the function that the params will be passed to.
        params = {
            OneM2MPrimitive.M2M_PARAM_TO: to,
            OneM2MPrimitive.M2M_PARAM_FROM: ae.aei,  # The AE-Credential-ID needs to be removed from the ae object
            OneM2MRequest.M2M_PARAM_RESOURCE_TYPE: OneM2MPrimitive.M2M_RESOURCE_TYPES.AE.value
        }

        # Remove AE-Credential-ID.
        ae.__dict__.pop(OneM2MPrimitive.M2M_PARAM_AE_ID)

        # Create a request object
        oneM2MRequest = OneM2MRequest()

        # Returns a OneM2MResponse object.  Handle any response code logic here.
        oneM2MResponse = oneM2MRequest.create(to, params, ae)

        # Return the AE instance or None if registration failed.
        # @todo return error msg or object with error msg.
        if oneM2MResponse.rsc == OneM2MPrimitive.M2M_RSC_CREATED:
            self.ae = AE(oneM2MResponse.pc)

        return oneM2MResponse

    def get_ae(self, ae_id: str):

        # Host and resource.
        to = '{}://{}:{}/PN_CSE/{}'.format(
            self.transport_protocol, self.host, self.port, ae_id
        )

        params = {
            OneM2MPrimitive.M2M_PARAM_FROM: ae_id,
            OneM2MRequest.M2M_PARAM_RESOURCE_TYPE: OneM2MPrimitive.M2M_RESOURCE_TYPES.AE.value
        }

        # Create a request object
        oneM2MRequest = OneM2MRequest()

        oneM2MResponse = oneM2MRequest.retrieve(to, params)

        if oneM2MResponse.rsc == OneM2MPrimitive.M2M_RSC_OK and oneM2MResponse.pc is not None:
            self.ae = AE(oneM2MResponse.pc)

        return oneM2MResponse

    def discover_resources(self):
        """ Synchronously discover containers registered with the CSE.

        Returns:
            list: A list of container resouce URIs or None.

        Raises:
            InvalidArgumentException: If the argument is not an AE.
        """
        # note: fu (filter usage) parameter required for resource discovery.
        to = self.get_to(self.rsc)

        # Create a request object.

        params = {
            OneM2MRequest.M2M_PARAM_FILTER_USAGE: 1,
            OneM2MRequest.M2M_PARAM_FROM: self.ae.ri,
            OneM2MRequest.M2M_PARAM_RESOURCE_TYPE: OneM2MPrimitive.M2M_RESOURCE_TYPES.Node.value
        }

        oneM2MRequest = OneM2MRequest(to, params)

        # Returns a OneM2MResponse object.  Handle any response code logic here.
        oneM2MResponse = oneM2MRequest.retrieve()

        return oneM2MResponse

    # @todo add possible rcn values to OneM2MResource class.
    def create_content_instance(self, uri: str, content: ContentInstance = None):
        """Create a content instance of a container resource.

        Args:
            uri: URI of a container resource.

        Returns:
            OneM2MResponse: The request response.
        """

        # Strip leading '/'
        uri = uri[1:] if uri[0] == '/' else uri

        to = self.get_to(uri)
        assert self.ae is not None
        params = {
            OneM2MPrimitive.M2M_PARAM_FROM: self.ae.ri,  # resource id.
            OneM2MPrimitive.M2M_PARAM_RESULT_CONTENT: OneM2MPrimitive.M2M_RESULT_CONTENT_TYPES.ChildResources,
            OneM2MPrimitive.M2M_PARAM_RESOURCE_TYPE: OneM2MPrimitive.M2M_RESOURCE_TYPES.ContentInstance.value,
        }

        content_instance = content

        oneM2MRequest = OneM2MRequest()

        oneM2MResponse = oneM2MRequest.create(to, params, content_instance)

        return oneM2MResponse

    def retrieve_content_instance(self, uri: str, rcn: int = 7):
        """Retrieves the latest content instance of a container resource.

        Args:
            uri: URI of a resource.

        Returns:
            OneM2MResponse: The request response.
        """

        to = self.get_to(uri)
        assert self.ae is not None
        params = {
            OneM2MPrimitive.M2M_PARAM_FROM: self.ae.ri,
            OneM2MRequest.M2M_PARAM_RESULT_CONTENT: OneM2MPrimitive.M2M_RESOURCE_TYPES.ContentInstance.value,
            OneM2MPrimitive.M2M_PARAM_RESOURCE_TYPE: OneM2MPrimitive.M2M_RESOURCE_TYPES.ContentInstance.value
        }

        oneM2MRequest = OneM2MRequest(to, params)

        oneM2MResponse = oneM2MRequest.retrieve()

        return oneM2MResponse

    def get_to(self, rsc: str):
        rsc = rsc[1:] if rsc[0] == '/' else rsc
        to = '{}://{}:{}/{}'.format(self.transport_protocol, self.host, self.port, rsc)
        return to

    def check_existing_subscriptions(self, uri: str, subscription_name: str):
        """Retrieve all existing subscriptions on a resource
        Args:
            uri: URI of a resource.

        Returns:
            OneM2MResponse: The request response.
        """
        to = self.get_to(uri)
        assert self.ae is not None
        params = {
            OneM2MPrimitive.M2M_PARAM_FROM: self.ae.ri,
            OneM2MPrimitive.M2M_PARAM_FILTER_USAGE: 1,
            OneM2MPrimitive.M2M_PARAM_RESOURCE_TYPE: OneM2MPrimitive.M2M_RESOURCE_TYPES.Subscription,
        }

        oneM2MRequest = OneM2MRequest(to, params)

        return oneM2MRequest.retrieve()

    def create_subscription(
        self, uri: str, sub_name: str, notification_uri: str = None, event_types: List[int] = [3], result_content=None
    ):
        """ Create a subscription to a resource.

        Args:
            uri: URI of a resource.

        Returns:
            OneM2MResponse: The request response.
        """

        json_data = {
            'enc': {'net': event_types, 'ty': 4},
            'nct': 1,
        }

        if notification_uri:
            json_data['nu'] = [notification_uri]

        return self.create_resource(
            uri,
            sub_name,
            Subscription(json_data),
            result_content
        )


    def create_resource(
        self, uri: str, name: str, content, result_content=None
    ):
        """ Create a resource.

        Args:
            uri: URI of a resource.

        Returns:
            OneM2MResponse: The request response.
        """

        to = self.get_to(uri)
        assert self.ae is not None
        params = {
            OneM2MPrimitive.M2M_PARAM_FROM: self.ae.ri,
        }

        if result_content is not None:
            params[OneM2MPrimitive.M2M_PARAM_RESULT_CONTENT] = result_content

        content.name = name

        oneM2MRequest = OneM2MRequest()

        oneM2MResponse = oneM2MRequest.create(to, params, content)

        return oneM2MResponse


    # @note: not really working.  'la' virtual resource never returns the latest content instance.
    def retrieve_latest_content_instance(self, uri: str):
        """Retrieve the latest content instance of a container.

        Args:
            uri: The container resource URI.

        Returns:
            An instance of ContentInstance or None if no content instance was found.

        Raises:
            ...
        """

        # Remove leading slash
        uri = uri[1:] if uri[0] == '/' else uri
        assert self.ae is not None
        to = '{}://{}:{}/{}/la'.format(
            self.transport_protocol, self.host, self.port, uri
        )

        params = {
            OneM2MPrimitive.M2M_PARAM_FROM: self.ae.ri,
        }

        oneM2MRequest = OneM2MRequest(to, params)

        oneM2MResponse = oneM2MRequest.retrieve()

        # How do you want to handle responses?
        if oneM2MResponse.uri == OneM2MPrimitive.M2M_RSC_OK:
            return ContentInstance(oneM2MResponse.pc['m2m:cin'])
        else:
            return None

    def retrieve_resource(self, uri: str, ty: OneM2MPrimitive.M2M_RESOURCE_TYPES):
        """ Synchronous retrieve resource request.

        Args:
            uri: The URI of the resource to retrieve.

        Returns:
            A OneM2MResource object.
        """

        to = self.get_to(uri)
        assert self.ae is not None
        params = {
            OneM2MPrimitive.M2M_PARAM_FROM: self.ae.ri,
            OneM2MRequest.M2M_PARAM_RESOURCE_TYPE: ty
        }

        oneM2MRequest = OneM2MRequest(to, params)

        oneM2MReponse = oneM2MRequest.retrieve()

        return oneM2MReponse

    def update_resource(self, uri: str, resource: OneM2MResource):
        """ Update a resource.

        Args:
            uri: The URI of the resource to retrieve.
            short_name:
            key:
            value:

        Returns:
            OneM2MResponse: The request response.
        """

        to = self.get_to(uri)

        assert self.ae is not None
        params = {
            OneM2MPrimitive.M2M_PARAM_FROM: self.ae.ri
        }

        oneM2MRequest = OneM2MRequest()

        oneM2MResponse = oneM2MRequest.update(to, params, resource)

        return oneM2MResponse

    def delete_ae(self):
        """ Delete ae.

        Returns:
            OneM2MResponse: The request response.
        """
        # Host and resource.
        to = '{}://{}:{}/{}/{}'.format(
            self.transport_protocol, self.host, self.port, self.rsc, self.ae.ri
        )

        # op is not required as it is implied by the function that the params will be passed to.
        params = {
            OneM2MPrimitive.M2M_PARAM_TO: to,
            OneM2MPrimitive.M2M_PARAM_FROM: self.ae.ri,
            OneM2MRequest.M2M_PARAM_RESOURCE_TYPE: OneM2MPrimitive.M2M_RESOURCE_TYPES.AE.value
        }

        # Create a request object
        oneM2MRequest = OneM2MRequest()

        # Returns a OneM2MResponse object.  Handle any response code logic here.
        oneM2MResponse = oneM2MRequest.delete(to, params)

        return oneM2MResponse

    def delete_resource(self, uri: str):
        """ Delete resource.

        Returns:
            OneM2MResponse: The request response.
        """
        # Host and resource.
        to = self.get_to(uri)

        # op is not required as it is implied by the function that the params will be passed to.
        assert self.ae is not None
        params = {
            OneM2MPrimitive.M2M_PARAM_TO: to,
            OneM2MPrimitive.M2M_PARAM_FROM: self.ae.ri,
        }

        # Create a request object
        oneM2MRequest = OneM2MRequest()

        # Returns a OneM2MResponse object.  Handle any response code logic here.
        return oneM2MRequest.delete(to, params)
