#!/usr/bin/env python

import requests, json

from client.OneM2M.http.HttpHeader import HttpHeader
from client.OneM2M.OneM2MPrimitive import OneM2MPrimitive
from client.OneM2M.OneM2MOperation import OneM2MOperation

class OneM2MResponse(OneM2MPrimitive):
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
        """Converts http response message to onem2m response primitive.
        """

        # Map headers to parameters.
        self._map_http_headers_to_m2m_params(http_response.headers)

        # Store the message body as the Content (pc) param. 
        self.pc= http_response.text
    
    def _map_http_headers_to_m2m_params(self, headers):
        """Converts HTTP headers onem2m2 response primitive params and stores them
           instance members.
        """

        # Filter out unsupported headers and convert them to their corresponding onem2m param.
        onem2m_params = { self.HTTP_HEADER_M2M_PARAM_TO_MAP[h]:v for h,v in headers.items() if h in self.SUPPORTED_HEADERS }

        # Store the params as instance members.
        self.__dict__ = onem2m_params