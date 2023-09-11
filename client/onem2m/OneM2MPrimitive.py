# Copyright (c) Aetheros, Inc.  See COPYRIGHT

#!/usr/bin/env python

from client.onem2m.OneM2MOperation import OneM2MOperation
from client.onem2m.http.HttpHeader import HttpHeader
from client.onem2m.http.HttpStatusCode import HttpStatusCode

import json
from enum import Enum, unique

class OneM2MPrimitive:
    CONTROL = 'control'
    CONTENT = 'content'

    CONTENT_TYPE_JSON = 'application/vnd.onem2m-res+json'

    # OneM2M HTTP HEADERS
    X_M2M_ORIGIN = 'X-M2M-Origin'
    X_M2M_RI     = 'X-M2M-RI'
    X_M2M_GID    = 'X-M2M-GID'
    X_M2M_RTU    = 'X-M2M-RTU'
    X_M2M_RTV    = 'X-M2M-RTV'
    X_M2M_OT     = 'X-M2M-OT'
    X_M2M_RST    = 'X-M2M-RST'
    X_M2M_RET    = 'X-M2M-RET'
    X_M2M_OET    = 'X-M2M-OET'
    X_M2M_EC     = 'X-M2M-EC'
    X_M2M_RSC    = 'X-M2M-RSC'
    X_M2M_ATI    = 'X-M2M-ATI'

    # OneM2M Parameters
    # @todo create response and request specific param tuples.
    # TS-0004 Table 8.2.2-1
    M2M_PARAM_TO                   = 'to'
    M2M_PARAM_FROM                 = 'fr'
    M2M_PARAM_OPERATION            = 'op'
    M2M_PARAM_REQUEST_IDENTIFIER   = 'rqi'
    M2M_PARAM_CONTENT              = 'cn'
    # M2M_PARAM_RESOURCE_TYPE      = 'rqt'
    M2M_PARAM_RESPONSE_STATUS_CODE = 'rsc'
    M2M_PARAM_AE_ID                = 'aei'
    M2M_PARAM_APP_ID               = 'api'
    M2M_PARAM_APP_NAME             = 'apn'
    M2M_PARAM_POINT_OF_ACCESS      = 'poa'

    # Query string request parameters.
    # M2M_PARAM_RESPONSE_TYPE      = 'rt'
    # M2M_PARAM_RESULT_PERSISTENCE = 'rp'
    M2M_PARAM_RESULT_CONTENT       = 'rcn'
    M2M_PARAM_FILTER_USAGE         = 'fu'
    M2M_PARAM_RESOURCE_NAME        = 'rn'
    M2M_PARAM_RESOURCE_TYPE        = 'ty'

    # @todo add remaining from TS-0009 Table 6.2.2.2-1

    M2M_HTTP_HEADERS = [
        X_M2M_ORIGIN,
        X_M2M_RI,
        X_M2M_GID,
        X_M2M_RTU,
        X_M2M_RTV,
        X_M2M_OT,
        X_M2M_RST,
        X_M2M_RET,
        X_M2M_OET,
        X_M2M_EC,
        X_M2M_RSC,
        X_M2M_ATI,
    ]

    # OneM2M Parameter to HTTP Header Map.
    M2M_PARAM_TO_HTTP_HEADER_MAP = {
        M2M_PARAM_TO: HttpHeader.URI,
        M2M_PARAM_OPERATION: HttpHeader.METHOD,
        M2M_PARAM_FROM: X_M2M_ORIGIN,
        M2M_PARAM_REQUEST_IDENTIFIER: X_M2M_RI,
        # X_M2M_RTV: X_M2M_RTV,
        # X_M2M_RTU: X_M2M_RTU
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
        OneM2MOperation.Create:   'POST',
        OneM2MOperation.Retrieve: 'GET',
        OneM2MOperation.Update:   'PUT',
        OneM2MOperation.Delete:   'DELETE',
        OneM2MOperation.Notify:   'POST',
    }

    # OneM2M Response Status Codes
    # @note all response codes should be declared as strings to avoid
    # casting response codes returned from the requests lib to strings
    # when handling request responses.
    M2M_RSC_OK =      '2000'
    M2M_RSC_CREATED = '2001'
    M2M_RSC_DELETED = '2002'
    M2M_RSC_UPDATED = '2004'
    # @todo add remaining status code from TS-0009 Table 6.3.2-1 'Status Code Mapping'

    M2M_REPONSE_STATUS_CODES = [
        M2M_RSC_OK,
        M2M_RSC_CREATED,
        M2M_RSC_DELETED,
        M2M_RSC_UPDATED,
    ]

    @unique
    class M2M_RESULT_CONTENT_TYPES(Enum):
        Nothing                               = 0
        Attributes                            = 1
        HierarchicalAddress                   = 2
        HierarchicalAddressPlusAttributes     = 3
        AttributesPlusChildResources          = 4
        AttributesPlusChildResourceReferences = 5
        ChildResourceReferences               = 6
        OriginalResource                      = 7
        ChildResources                        = 8

    @unique
    class M2M_RESOURCE_TYPES(Enum):
        Mixed                                 = 0
        AccessControlPolicy                   = 1
        AE                                    = 2
        Container                             = 3
        ContentInstance                       = 4
        CSEBase                               = 5
        Delivery                              = 6
        EventConfig                           = 7
        ExecInstance                          = 8
        Group                                 = 9
        LocationPolicy                        = 10
        M2MServiceSubscription                = 11
        MgmtCmd                               = 12
        MgmtObj                               = 13
        Node                                  = 14
        PollingChannel                        = 15
        RemoteCSE                             = 16
        Request                               = 17
        Schedule                              = 18
        ServiceSubscribedAppRule              = 19
        ServiceSubscribedNode                 = 20
        StatsCollect                          = 21
        StatsConfig                           = 22
        Subscription                          = 23
        SemanticDescriptor                    = 24
        NotificationTargetMgmtPolicyRef       = 25
        NotificationTargetPolicy              = 26
        PolicyDeletionRules                   = 27
        FlexContainer                         = 28
        TimeSeries                            = 29
        TimeSeriesInstance                    = 30
        Role                                  = 31
        Token                                 = 32
        TrafficPattern                        = 33
        DynamicAuthorizationConsultation      = 34
        AccessControlPolicyAnnc               = 10001
        AEAnnc                                = 10002
        ContainerAnnc                         = 10003
        ContentInstanceAnnc                   = 10004
        GroupAnnc                             = 10009
        LocationPolicyAnnc                    = 10010
        MgmtObjAnnc                           = 10013
        NodeAnnc                              = 10014
        RemoteCSEAnnc                         = 10016
        ScheduleAnnc                          = 10018
        SemanticDescriptorAnnc                = 10024
        FlexContainerAnnc                     = 10028
        TimeSeriesAnnc                        = 10029
        TimeSeriesInstanceAnnc                = 10030
        TrafficPatternAnnc                    = 10033
        DynamicAuthorizationConsultationAnnc  = 10034


    @unique
    class M2M_FILTER_USAGE(Enum):
        Unspecified                           = -1
        Discovery                             = 1
        ConditionalRetrieval                  = 2
        IpeonDemandDiscovery                  = 3


    @unique
    class M2M_NOTIFICATION_EVENT_TYPES(Enum):
        Unspecified                                    = -1
        UpdateOfResource                               = 1
        DeleteOfResource                               = 2
        CreateOfDirectChildResource                    = 3
        DeleteOfDirectChildResource                    = 4
        RetrieveOfContainerResourceWithNoChildResource = 5


    def __str__(self):
        return json.dumps(self.__dict__)


class MissingRequiredControlParams(Exception):
    def __init__(self, msg: str):
        self.msg = msg