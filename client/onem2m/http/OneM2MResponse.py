#!/usr/bin/env python

import requests, json

from client.onem2m.http.HttpHeader import HttpHeader
from client.onem2m.OneM2MPrimitive import OneM2MPrimitive, MissingRequiredControlParams
from client.onem2m.OneM2MOperation import OneM2MOperation
from client.onem2m.OneM2MResource import OneM2MResource


class OneM2MResponse(OneM2MPrimitive):
    # An exception will be thrown if the http_response object from the requests
    # lib is missing any of the required control or content params listed here.
    # @todo add remaining params.
    REQUIRED_PARAMS = {
        OneM2MPrimitive.CONTROL: [
            OneM2MPrimitive.X_M2M_ORIGIN,
            OneM2MPrimitive.X_M2M_RI,
            OneM2MPrimitive.X_M2M_RSC,
        ],
        OneM2MPrimitive.CONTENT: [
            OneM2MResource.M2M_ATTR_PRIMITIVE_CONTENT,  # 'pc' in body
            # This is not really enforced and not necessary...
        ],
    }

    # The HTTP headers listed here will be converted to their corresponding
    # onem2m parameter.
    # If a header is not included here, it will be ignored.
    # TS-0009 6.4.0
    SUPPORTED_HEADERS = [
        # HttpHeader.HOST,
        # HttpHeader.ACCEPT,
        # HttpHeader.CONTENT_TYPE, # Only present in requests if message contains a message-body
        HttpHeader.CONTENT_LOCATION,
        # HttpHeader.CONTENT_LENGTH,
        # # HttpHeader.ETAG,
        OneM2MPrimitive.X_M2M_ORIGIN,
        OneM2MPrimitive.X_M2M_RI,
        # OneM2MPrimitive.X_M2M_GID,
        # OneM2MPrimitive.X_M2M_RTU,
        # OneM2MPrimitive.X_M2M_OT,
        # OneM2MPrimitive.X_M2M_RST,
        # OneM2MPrimitive.X_M2M_RET,
        # OneM2MPrimitive.X_M2M_OET,
        # OneM2MPrimitive.X_M2M_EC,
        OneM2MPrimitive.X_M2M_RSC,
        # OneM2MPrimitive.X_M2M_ATI
    ]

    def __init__(self, http_response):
        """Converts HTTP response message to onem2m response primitive.

        Args:
            http_response: requests response instance.
        """

        http_response.raise_for_status()

        try:
            self.pc = None

            # Map headers to parameters.
            # Raises MissingRequiredControlParams exception if a required control header is missing.
            self._map_http_headers_to_m2m_params(http_response.headers)

            # Store the message body as the Content (pc) param.
            if 'Content-Type' in http_response.headers and 'json' in http_response.headers['Content-Type']:
                self.pc = json.loads(http_response.text)

        except Exception as e:
            print(e)
            print(http_response)
            print(http_response.text)
            raise

    def _map_http_headers_to_m2m_params(self, headers):
        """Converts HTTP headers onem2m2 response primitive params and stores them
           instance members.

        Raises:
            MissingRequiredControlParams: If required params from control section are missing.
        """

        # Ensure all required control params were included.
        missing_control_params = []

        for required_param in self.REQUIRED_PARAMS[OneM2MPrimitive.CONTROL]:
            if required_param not in headers.keys():
                missing_control_params.append(required_param)

        if len(missing_control_params):
            raise MissingRequiredControlParams(
                'On2M2M Response Primitive Missing required control param(s) {}'.format(
                    missing_control_params
                )
            )

        # Filter out unsupported headers and convert them to their corresponding onem2m param.
        # @note returns a list of tuples ('param': 'value')
        # @todo refactor tuples into OneM2MParam class instances.
        onem2m_params = {
            self.HTTP_HEADER_M2M_PARAM_TO_MAP[h]: v
            for h, v in headers.items()
            if h in self.SUPPORTED_HEADERS
        }

        # Store the params as instance members.
        self.__dict__ = onem2m_params
