#!/usr/bin/env python

from client.OneM2M.OneM2MOperation import OneM2MOperation
from client.OneM2M.http.HttpHeader import HttpHeader
from client.OneM2M.http.HttpStatusCode import HttpStatusCode

class OneM2MPrimitive():
    CONTENT_TYPE_JSON = 'application/vnd.onem2m-res+json; ty=2'

    # OneM2M HTTP HEADERS
    X_M2M_ORIGIN = 'X-M2M-Origin'
    X_M2M_RI = 'X-M2M-RI'
    X_M2M_GID = 'X-M2M-GID'
    X_M2M_RTU = 'X-M2M-RTU'
    X_M2M_OT = 'X-M2M-OT'
    X_M2M_RST = 'X-M2M-RST'
    X_M2M_RET = 'X-M2M-RET'
    X_M2M_OET = 'X-M2M-OET'
    X_M2M_EC = 'X-M2M-EC'
    X_M2M_RSC = 'X-M2M-RSC'
    X_M2M_ATI = 'X-M2M-ATI'

    # OneM2M Parameters
    # @todo create response and request specific param tuples.
    # TS-0004 Table 8.2.2-1
    M2M_PARAM_TO = 'to'
    M2M_PARAM_FROM = 'fr'
    M2M_PARAM_OPERATION = 'op'
    M2M_PARAM_REQUEST_IDENTIFIER = 'rqi'
    M2M_PARAM_CONTENT = 'cn'
    M2M_PARAM_RESOURCE_TYPE = 'rqt'
    M2M_PARAM_RESPONSE_STATUS_CODE= 'rsc'

    # Query string request parameters.
    RESPONSE_TYPE = 'rt'
    RESULT_PERSISTENCE = 'rp'
    # @todo add remaining from TS-0009 Table 6.2.2.2-1 

    # OneM2M Parameter to HTTP Header Map.
    M2M_PARAM_TO_HTTP_HEADER_MAP = {
        M2M_PARAM_TO: HttpHeader.URI,
        M2M_PARAM_FROM: X_M2M_ORIGIN,
        M2M_PARAM_OPERATION: HttpHeader.METHOD,
        M2M_PARAM_REQUEST_IDENTIFIER: X_M2M_RI
    }

    # HTTP Header to OneM2M Parameter Map.
    HTTP_HEADER_M2M_PARAM_TO_MAP = {
        # HttpHeader.URI: M2M_PARAM_TO,
        # X_M2M_ORIGIN: M2M_PARAM_FROM,
        # HttpHeader.METHOD: M2M_PARAM_OPERATION,
        # X_M2M_RI: M2M_PARAM_REQUEST_IDENTIFIER,
        
        # HttpHeader.HOST,
        # HttpHeader.ACCEPT,
        # HttpHeader.CONTENT_TYPE,
        HttpHeader.CONTENT_LOCATION: M2M_PARAM_CONTENT,
        # HttpHeader.CONTENT_LENGTH,
        # HttpHeader.ETAG,
        X_M2M_ORIGIN: M2M_PARAM_FROM,
        X_M2M_RI: M2M_PARAM_REQUEST_IDENTIFIER,
        # X_M2M_GID,
        # X_M2M_RTU,
        # X_M2M_OT,
        # X_M2M_RST,
        # X_M2M_RET,
        # X_M2M_OET,
        # X_M2M_EC,
        X_M2M_RSC: M2M_PARAM_RESPONSE_STATUS_CODE,
        # X_M2M_ATI
    }

    # TS-0009-V2.6.1 6.2.1
    # {
    #   ONE_M2M_OPERATION: HTTP_METHOD
    # }
    OPS_TO_METHOD_MAPPING = {
        OneM2MOperation.Create: 'POST',
        OneM2MOperation.Retrieve: 'GET',
        OneM2MOperation.Update: 'PUT',
        OneM2MOperation.Delete: 'DELETE',
        OneM2MOperation.Notify: 'POST',
    }

    # OneM2M Response Status Codes
    M2M_RSC_OK = 2000
    M2M_RSC_CREATED = 2001
    M2M_RSC_DELETED = 2002
    M2M_RSC_UPDATED = 2004

    M2M_REPONSE_STATUS_CODES = [
        M2M_RSC_OK,
        M2M_RSC_CREATED,
        M2M_RSC_DELETED,
        M2M_RSC_UPDATED
    ]