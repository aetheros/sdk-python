#!/usr/bin/env python

import requests, aiohttp, json, random

from client.OneM2M.OneM2MPrimitive import OneM2MPrimitive
from client.OneM2M.OneM2MOperation import OneM2MOperation
from client.OneM2M.http.OneM2MResponse import OneM2MResponse
from client.OneM2M.OneM2MResource import OneM2MResource
from client.exceptions.BaseException import BaseException
from client.OneM2M.http.HttpHeader import HttpHeader

class OneM2MRequest(OneM2MPrimitive):
    """OneM2M request primitive to http mapping.
    """ 

    # Result content args.
    # @todo move these to their own class?
    M2M_RCN_NOTHING = 0
    M2M_RCN_UNSPECIFIED = 1
    M2M_RCN_ATTRIBUTES = 1
    M2M_RCN_HIERARCHICAL_ADDRESS = 2
    M2M_RCN_HIERARCHICAL_ADDRESS_ATTRIBUTES = 3
    M2M_RCN_ATTRIBUTES_CHILD_RESOURCES = 4
    M2M_RCN_ATTRIBUTES_CHILD_RESOURCE_REFERENCES = 5
    M2M_RCN_CHILD_RESOURCE_REFERENCES = 6
    M2M_RCN_ORIGINAL_RESOURCE = 7
    M2M_RCN_CHILD_RESOURCES = 8

    M2M_RCN = [
        M2M_RCN_NOTHING,
        M2M_RCN_UNSPECIFIED,
        M2M_RCN_ATTRIBUTES,
        M2M_RCN_HIERARCHICAL_ADDRESS,
        M2M_RCN_HIERARCHICAL_ADDRESS_ATTRIBUTES,
        M2M_RCN_ATTRIBUTES_CHILD_RESOURCES,
        M2M_RCN_ATTRIBUTES_CHILD_RESOURCE_REFERENCES,
        M2M_RCN_CHILD_RESOURCE_REFERENCES,
        M2M_RCN_ORIGINAL_RESOURCE,
        M2M_RCN_CHILD_RESOURCES
    ]
    # ./@todo move these to their own class?

    # Required parameters for each onem2m operation.  If a requested operation's params
    # does not contain all of the corresponding parameters outline here, the function 
    # performing the operation will raise an RequiredRequestParameterMissingException. 
    REQUIRED_HTTP_PARAMS = {
        OneM2MOperation.Create: [
            # OneM2MPrimitive.M2M_PARAM_OPERATION, # Implied by the function name.
            OneM2MPrimitive.M2M_PARAM_TO, # Set in the constructor or the function.
            OneM2MPrimitive.M2M_PARAM_FROM, # Set in the constructor?
            OneM2MPrimitive.M2M_PARAM_REQUEST_IDENTIFIER, # Generated dynamically.
            # OneM2MPrimitive.M2M_PARAM_RESOURCE_TYPE # Set in the constructor
        ],
        OneM2MOperation.Retrieve: [],
        OneM2MOperation.Update: [],
        OneM2MOperation.Delete: [],
        OneM2MOperation.Notify: []
    }
    

    # Query string param shortnames.
    # TS-0009-V2.6.1 Table 6.2.2.1-1
    M2M_PARAM_RESPONSE_TYPE = 'rt'
    M2M_PARAM_RESULT_PERSISTENCE = 'rp'
    M2M_PARAM_RESULT_CONTENT = 'rcn'
    M2M_PARAM_DELIVERY_AGGREGATION = 'da'
    M2M_PARAM_CREATED_BEFORE = 'crb'
    M2M_PARAM_CREATED_AFTER = 'cra'
    M2M_PARAM_MODIFIED_SINCE = 'ms'
    M2M_PARAM_UNMODIFIED_SINCE = 'us'
    M2M_PARAM_STATE_TAG_SMALLER = 'sts'
    M2M_PARAM_STATE_TAG_BIGGER = 'stb'
    M2M_PARAM_EXPIRE_BEFORE = 'exb'
    M2M_PARAM_EXPIRE_AFTER = 'exa'
    M2M_PARAM_LABELS = 'lbl'
    M2M_PARAM_RESOURCE_TYPE = 'ty'
    M2M_PARAM_SIZE_ABOVE = 'sza'
    M2M_PARAM_SIZE_BELOW = 'szb'
    M2M_PARAM_CONTENT_TYPE = 'cty'
    M2M_PARAM_LIMIT = 'lim'
    M2M_PARAM_ATTRIBUTE = 'atr'
    M2M_PARAM_FILTER_USAGE = 'fu'
    M2M_PARAM_SEMANTICS_FILTER = 'smf'
    M2M_PARAM_DISCOVERY_RESULT_TYPE = 'drt'
    M2M_PARAM_ROLE_IDS = 'rids'
    M2M_PARAM_TOKEN_IDS = 'tids'
    M2M_PARAM_LOCAL_TOKEN_IDS = 'ltids'
    M2M_PARAM_TOKEN_REQUEST_INDICATOR = 'tqi'

    # Request params (query string).
    QUERY_STRING_PARAMS = [
        M2M_PARAM_RESPONSE_TYPE,
        M2M_PARAM_RESULT_PERSISTENCE,
        M2M_PARAM_RESULT_CONTENT,
        M2M_PARAM_DELIVERY_AGGREGATION,
        M2M_PARAM_CREATED_BEFORE,
        M2M_PARAM_CREATED_AFTER,
        M2M_PARAM_MODIFIED_SINCE,
        M2M_PARAM_UNMODIFIED_SINCE,
        M2M_PARAM_STATE_TAG_SMALLER,
        M2M_PARAM_STATE_TAG_BIGGER,
        M2M_PARAM_EXPIRE_BEFORE,
        M2M_PARAM_EXPIRE_AFTER,
        M2M_PARAM_LABELS,
        M2M_PARAM_RESOURCE_TYPE,
        M2M_PARAM_SIZE_ABOVE,
        M2M_PARAM_SIZE_BELOW,
        M2M_PARAM_CONTENT_TYPE,
        M2M_PARAM_LIMIT,
        M2M_PARAM_ATTRIBUTE,
        M2M_PARAM_FILTER_USAGE,
        M2M_PARAM_SEMANTICS_FILTER,
        M2M_PARAM_DISCOVERY_RESULT_TYPE,
        M2M_PARAM_ROLE_IDS,
        M2M_PARAM_TOKEN_IDS,
        M2M_PARAM_LOCAL_TOKEN_IDS,
        M2M_PARAM_TOKEN_REQUEST_INDICATOR
    ]

    def __init__(self, to=None, params={}):
        """ Constructor.
           Args:
            to: The cse host
            params: The request params to convert to http headers.
        """

        # Target host.
        self.to = to

        # No param requirements can be enforced because we dont know the requested operation
        # that will be performed yet.  OneM2M operations are dictated by the member function that is
        # called on the instance and param validation is performed in those functions.
        self.params = params
                
    def _validate_required_params(self, operation=None, params=None):
        """Validates the required parameters (HTTP mapped ones only) for a specified OneM2M operation (Create, Retrieve, ect).
        
        Args:
            op: The OneM2M operation to validate for.
            params: The request params to validate.

        Raises:
            RequiredRequestParameterMissingException: If a required parameter is missing.
        """

        # Get the request params keys.
        request_params = tuple(params.keys())
        # Determine the operation.  Operation and parameters can be specified in the constructor and then overriden
        # in the actual call to the request function (create, retrieve, ect...)
        request_operation = params[OneM2MPrimitive.M2M_PARAM_OPERATION] if operation is None else operation
        # Get the required parameters for the specified operation.
        required_params = self.REQUIRED_HTTP_PARAMS[request_operation]

        # Raise an exception if a required param is missing in the request.
        for param in required_params:
            if param not in request_params:
                raise RequiredRequestParameterMissingException(operation, param)

    def _validate_query_string_param(self, name, value):
        """Validates query string parameters are valid.

        Args:
            name: The parameter name.
            value: The value of the parameter.

        Return:
             Always True unless preempted by an exception.

        Raises:
            InvalidOneM2MRequestParameterException: If the parameter name is not valid.
            InvalidOneM2MRequestParameterValueException: If the parameter value is invalid (0..1 || 0..N) @todo
        """
        if name not in OneM2MRequest.QUERY_STRING_PARAMS:
            raise InvalidOneM2MRequestParameterException(name)

        return True

        # @todo add param value validation base on muliplicity
        # TS-0009-V2.6.1 Table 6.2.2.2-1 query string param values.  Do validation on header values too (are there value constraints)?

    def _map_params_to_headers(self, params):
        """ Converts a OneM2M request parameters to their corresponding HTTP headers.
            If the submitted argument contains request parameters that DO NOT map to a 
            HTTP header, they will be silently ignored.

        Args:
            params: The OneM2M request parameters to convert to HTTP headers.

        Returns:
            A dict of HTTP headers and values.
        """

        # Header dict to build and return.
        header = {}

        # Build the request headers.
        for param, value in params.items():
            # Perform any validation or transformation on request values here.
            if param is OneM2MPrimitive.M2M_PARAM_OPERATION:
                value = OneM2MPrimitive.OPS_TO_METHOD_MAPPING[value] # Transform onem2m operation to http method.

            # Avoid key exception on params that map query strings.  Map only existing values.  Ignore any params not
            # explicitly defined as having a http header mapping in the M2M_PARAM_TO_HTTP_HEADER_MAP dict.
            if param in OneM2MPrimitive.M2M_PARAM_TO_HTTP_HEADER_MAP.keys():
                header[OneM2MPrimitive.M2M_PARAM_TO_HTTP_HEADER_MAP[param]] = str(value)

        return header

    def _map_params_to_query_string(self, to, params):
        """Maps OneM2M parameters to their query string representation and appends them to 'to'.

        Args:
            to: The 'to' param
            params: A params dict

        Returns:
             The 'to' string with the query string arguments appended to it.
        """

        # Strip query string in event its already been applied and append the query string indicator.
        to = to.split('?')[0] + '?'

        for param, value in params.items():
            if param in OneM2MRequest.QUERY_STRING_PARAMS and self._validate_query_string_param(param, value): # Throws
                if to[-1] != '?':
                    to += '&'
                to += '{}={}'.format(param, value)
        
        # No query string, strip the '? and return the just 'to'.  Otherwise, return the modified to with query string.
        return to[:-1] if to[-1] == '?' else to  

    def _resolve_params(self, to, params):
        """Resolves 'to' and 'params' arguments according to a hierachy:
           1) 'to' and 'param' arguments that are explicitly set here
               override the 'to' and 'param' members set in the constuctor, but
               are NOT PERSISTED to any following requests. 
           2) If 'to' is None, then 'params' is checked for 'to' and used.  If no 'to'
              is found in 'params' or 'params' are None, the member 'to' and 'params' set in the
              constructor are used.

        Args:
            to: The 'to' param
            param: The remaining params

        Returns:
            The resolved 'to' (string), params (dict).

        Raises:
            InvalidRequestParameterStructureException: If the params argument is not a dict.
        """
        # Use the params set in the constructor.
        if params is None:
            params = self.params

        # Generate a random request id.
        params[OneM2MPrimitive.M2M_PARAM_REQUEST_IDENTIFIER] = self._generate_rqi()

        # Params must be expressed as a dict.
        if isinstance(params, dict) is False:
            raise InvalidRequestParameterStructureException(params)

        # Use params 'to'.
        if to is None:
            # If params contains to...
            if OneM2MPrimitive.M2M_PARAM_TO in params.keys():
                # to param will be removed in _map_params_to_headers.
                to = params[OneM2MPrimitive.M2M_PARAM_TO]
            else:
                if to is None:
                    to = self.to

        if OneM2MPrimitive.M2M_PARAM_TO not in params.keys():
            params[OneM2MPrimitive.M2M_PARAM_TO] = to

        to = self._map_params_to_query_string(to, params)

        return to, params

    def _get_all_request_params(self):
        """Aggregates all of the query string and header request params.

        Returns: A list of all param names.
        """
        return sum(self.REQUIRED_HTTP_PARAMS.values(), self.QUERY_STRING_PARAMS)

    def set_param(self, param, value=None):
        """Sets a request parameter.

           Args:
            param: The param name
            value: The param value

           Raises:
            InvalidOneM2MRequestParameterException: If the params argument is not a dict.
        """
        # Check if a dict of params was passed in.
        if value is None and type(param) is dict:
            for p, v in param.items():
                # Dont allow invalid request params, but dont throw an exception.  Ignore and log.
                if p in self._get_all_request_params():
                    self.params[p] = v
                else:
                    # @todo do some logging
                    pass
        else:
            # Dont allow invalid request params, but dont throw an exception.  Ignore and log.
            if param in self._get_all_request_params():
                # @todo perform some validation...
                self.params[param] = value
            else:
                # @todo do some logging
                pass

    def create(self, to=None, params=None, content=None):
        """ Synchronous OneM2M Create request.
        
        Args:
            to: Host (Overrides 'to' argument set in constructor.)
            params: Dict of OneM2MParams (Overrides 'params' argument set in constructor.)
            content: A OneM2MResource

        Returns:
            A OneM2MResponse object.

        Raises:
            RequiredRequestParameterMissingException: If a required parameter is not is not included.
        """

        # Process arguments.
        to, params = self._resolve_params(to, params)

        # If params is set to None, check if the instance was initialized with paramters.
        # Raises an RequiredRequestParameterMissingException.
        self._validate_required_params(OneM2MOperation.Create, params)

        # Convert OneM2M request params to headers for HTTP request.
        headers = self._map_params_to_headers(params)

        # Set the content type for the request.
        # @todo move this to member with setter function.
        headers[HttpHeader.CONTENT_TYPE] = OneM2MPrimitive.CONTENT_TYPE_JSON

        # Extract entity members as dict.
        if isinstance(content, OneM2MResource):
            # Wrap the entity in a container json object
            # entity_name = content.__class__.__name__.lower()
             # @todo raise an ShortNameNotSet (OneM2MResource) expection.
            entity_name = content.short_name
            data = {entity_name: content.get_content()}

            # Serialize dict. @todo data serialization must be dictated by content-type
            data = json.dumps(data)

            # HTTP POST implied by OneM2M Create Operation (function signature).
            http_response = requests.post(to, headers=headers, data=data)
        else:
            # HTTP POST implied by OneM2M Create Operation (function signature).
            http_response = requests.post(to, headers=headers)

        # Return a OneM2MResponse instance.
        return OneM2MResponse(http_response)

    def update(self, to=None, params=None, short_name=None, key=None, value=None):
        """ Synchronous OneM2M update request.
        
        Args:
            to: Host (Overrides 'to' argument set in constructor.)
            params: Dict of OneM2MParams (Overrides 'params' argument set in constructor.)
            short_name: Short name of the resource type.
            key: Attribute to update.
            value: New value of the attribute.

        Returns:
            A OneM2MResponse object.

        Raises:
            RequiredRequestParameterMissingException: If a required parameter is not is not included.
        """

        # Process arguments.
        to, params = self._resolve_params(to, params)

        # If params is set to None, check if the instance was initialized with paramters.
        # Raises an RequiredRequestParameterMissingException.
        self._validate_required_params(OneM2MOperation.Create, params)

        # Convert OneM2M request params to headers for HTTP request.
        headers = self._map_params_to_headers(params)

        # Set the content type for the request.
        # @todo move this to member with setter function.
        headers[HttpHeader.CONTENT_TYPE] = OneM2MPrimitive.CONTENT_TYPE_JSON

        data = {
            short_name: {
                key: value
            }
        }

        # Serialize dict. @todo data serialization must be dictated by content-type
        data = json.dumps(data)

            # HTTP POST implied by OneM2M Create Operation (function signature).
        http_response = requests.put(to, headers=headers, data=data)

        # Return a OneM2MResponse instance.
        return OneM2MResponse(http_response)

    def retrieve(self, to=None, params=None):
        """ Synchronous OneM2M Retrieve request.
        
        Args:
            to: Host (Overrides 'to' argument set in constructor.)
            params: Dict of OneM2MParams (Overrides 'params' argument set in constructor.)
            content: A OneM2MResource

        Returns:
            A OneM2MResponse object.

        Raises:
            RequiredRequestParameterMissingException: If a required parameter is not is not included.
        """

        # Process arguments.
        to, params = self._resolve_params(to, params)

        # If params is set to None, check if the instance was initialized with paramters.
        # Raises an RequiredRequestParameterMissingException.
        self._validate_required_params(OneM2MOperation.Retrieve, params)

        # Convert OneM2M request params to headers for HTTP request.
        headers = self._map_params_to_headers(params)

        # Set the content type for the request.
        # @todo move this to member with setter function.
        headers[HttpHeader.CONTENT_TYPE] = OneM2MPrimitive.CONTENT_TYPE_JSON
 
        # HTTP GET implied by OneM2M retrieve Operation (function signature).
        http_response = requests.get(to, headers=headers)

        # Return a OneM2MResponse instance.
        return OneM2MResponse(http_response)

    def delete(self, to=None, params=None):
        """ Synchronous OneM2M Delete operation.
        
        Args:
            to: Host (Overrides 'to' argument set in constructor.)
            param: Dict of OneM2MParams (Overrides 'params' argument set in constructor.)

        Returns:
            A OneM2MResponse object.
        """

        # Process arguments.
        to, params = self._resolve_params(to, params)

        # If params is set to None, check if the instance was initialized with paramters.
        # Raises an exception @todo implement MissingRequiredParamException.
        self._validate_required_params(OneM2MOperation.Delete, params)

        # Build headers for HTTP request.
        headers = self._map_params_to_headers(params)

        # Set the content type for the request.
        # @todo move this to member with setter function.
        headers[HttpHeader.CONTENT_TYPE] = OneM2MPrimitive.CONTENT_TYPE_JSON

        # HTTP POST implied by OneM2M Create Operation (function signature).
        http_response = requests.delete(to, headers=headers)

        # Return a OneM2MResponse instance.
        return OneM2MResponse(http_response)

    def notify(self, to=None, params=None):
        pass

    async def create_async(self, to, params=None, content=None):
        """Asynchronous create (POST) OneM2M request.

        Args:
            to: Host (Overrides 'to' argument set in constructor.)
            param: Dict of OneM2MParams (Overrides 'params' argument set in constructor.)
            content: ...

        Returns:
            A OneM2MResponse object.
        """
        # Ensure form of params.
        if params is not None and isinstance(params, dict) is False:
            raise Exception('Headers must be dict')

        # If params is set to None, check if the instance was initialized with paramters.
        # Raises an exception @todo implement MissingRequiredParamException.
        self._validate_required_params(OneM2MOperation.Create, params)
        
        async with aiohttp.ClientSession() as session:
            async with session.get(to) as resp:
                # Map the client response to the OneM2MResponse.
                return resp

    def _generate_rqi(self):
        """Generate a random request id.

        Returns:
            str: Request id.
        """
        return str(random.randrange(1000000,999999999999))


class InvalidOneM2MRequestParameterException(BaseException):
    def __init__(self, param):
        self.message = '{} is not a valid OneM2M request parameter.'.format(param)

class RequiredRequestParameterMissingException(BaseException):
    def __init__(self, op, param):
        """Missing required parameter from a OneM2M request.
        
        Args:
            op: OneM2M operation
            param: Missing param
        """
        
        self.op = op
        self.param = param
        self.msg = 'The "{}" op requires the "{}" param be included in the request.'.format(op, param)

class InvalidRequestParameterStructureException(BaseException):
    def __init__(self, obj):
        """Request parameter structure must be dict exception.

           Args:
            obj: The object passed as the request parameters.
        """
        self.type = obj.__class__.__name__
        self.msg = 'Request "params" must be a dict. {} recieved.'.format(self.type)

class InvalidOneM2MOperationException(BaseException):
    def __init__(self, msg):
        self.message = msg