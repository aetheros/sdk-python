#!/usr/bin/env python

import unittest, asyncio

from client.onem2m.OneM2MPrimitive import OneM2MPrimitive
from client.onem2m.http.OneM2MRequest import OneM2MRequest
from client.onem2m.OneM2MOperation import OneM2MOperation
from client.exceptions.InvalidOneM2MOperationException import InvalidOneM2MOperationException
from client.exceptions.RequiredRequestParameterMissingException import RequiredRequestParameterMissingException
from client.exceptions.InvalidRequestParameterStructureException import InvalidRequestParameterStructureException

class OneM2MRequestTests(unittest.TestCase):
    # def setUp(self):
    #     """Setup async loop.
    #     """
    #     self.loop = asyncio.new_event_loop()
    #     asyncio.set_event_loop(None)

    def test_map_params_to_header(self):
        """_map_params_to_headers(params): OneM2M parameters correctly map to their corresponding HTTP headers.
        """
        print(self.shortDescription())

        params = {
            OneM2MPrimitive.M2M_PARAM_TO: 'http://localhost:8000',
            OneM2MPrimitive.M2M_PARAM_FROM: 'http://localhost:8001',
            OneM2MPrimitive.M2M_PARAM_REQUEST_IDENTIFIER: '123',
        }

        req = OneM2MRequest()

        # Convert the params to headers.
        headers = req._map_params_to_headers(params)
        
        # Compare the headers values using their keys to the params values.
        for header in req.HTTP_HEADER_M2M_PARAM_TO_MAP:
            if header in headers.keys():
                http_header = headers[header]
                onem2m_param = params[req.HTTP_HEADER_M2M_PARAM_TO_MAP[header]]

                self.assertEqual(onem2m_param, http_header)
    
    def test_validate_required_params_for_create_op(self):
        """_validate_required_params(OneM2MOperation.Create, params): Raises exception when a required param is missing from a Create operation request.
        """
        print(self.shortDescription())

        # Operation to validate params for.
        op = OneM2MOperation.Create
        missing_required_param = OneM2MPrimitive.M2M_PARAM_FROM

        # Invalid due to missing required param.
        params = {
            OneM2MPrimitive.M2M_PARAM_TO: 'http://localhost:8000',
            OneM2MPrimitive.M2M_PARAM_REQUEST_IDENTIFIER: '123',
        }

        req = OneM2MRequest()

        try:
            req._validate_required_params(op, params)
        except RequiredRequestParameterMissingException as err:
            # Catch the exception and ensure op and offending param are correct.
            self.assertEqual(err.op, op, 'Incorrect operation specified in {}.  {} should be {}.'.format(err.__class__.__name__, err.op, op))
            self.assertEqual(err.param, missing_required_param, 'Incorrect missing param specified in {}.  {} should be {}.'.format(err.__class__.__name__, err.param, missing_required_param))

    def test_resolve_params_uses_params_to_when_to_arg_is_none(self):
        """_resolve_params(to=None, params=original_params): Uses the 'to' from 'params' when the 'to' function arg is None.
        """
        print(self.shortDescription())

        # Operation to validate params for.
        op = OneM2MOperation.Create

        # Invalid due to missing required param.
        original_params = {
            OneM2MPrimitive.M2M_PARAM_TO: 'http://localhost:8000',
            OneM2MPrimitive.M2M_PARAM_REQUEST_IDENTIFIER: '123',
        }

        req = OneM2MRequest()

        to, params = req._resolve_params(to=None, params=original_params)

        self.assertEqual(original_params[OneM2MPrimitive.M2M_PARAM_TO], to, '"to" does not match value specified in "params". {} != {}'.format(original_params[OneM2MPrimitive.M2M_PARAM_TO],to))
        self.assertEqual(original_params, params, '"params" has been corrupted. {} != {}'.format(original_params, params))

    def test_resolve_params_uses_member_params_to_when_to_arg_is_none_and_params_has_no_to(self):
        """_resolve_params(to=None, params=original_params): Uses the 'to' from member 'params' when the 'to' function arg is None and 'params' arg does not contain a 'to' member.
        """
        print(self.shortDescription())

        # Operation to validate params for.
        op = OneM2MOperation.Create
        arg_to = 'http://localhost:8080'

        # Invalid due to missing required param.
        original_params = {
            OneM2MPrimitive.M2M_PARAM_REQUEST_IDENTIFIER: '123',
        }

        req = OneM2MRequest()

        to, params = req._resolve_params(to=arg_to, params=original_params)

        self.assertEqual(arg_to, to, '"to" does not match value specified in "params". {} != {}'.format(arg_to, to))
        self.assertEqual(original_params, params, '"params" has been corrupted. {} != {}'.format(original_params, params))

    def test_resolve_params_to_arg_overrides_params_and_member_to(self):
        """_resolve_params(to, params): 'to' from function argument overrides all 'params' 'to' members.
        """
        print(self.shortDescription())

        # Operation to validate params for.
        op = OneM2MOperation.Create

        correct_to = 'http://correctto.com:8080'

        # Invalid due to missing required param.
        original_params = {
            OneM2MPrimitive.M2M_PARAM_TO: 'http://localhost:8000',
            OneM2MPrimitive.M2M_PARAM_REQUEST_IDENTIFIER: '123',
        }

        req = OneM2MRequest()

        to, params = req._resolve_params(to=correct_to, params=original_params)

        self.assertEqual(correct_to, to, '"to" does not match value specified in "params". {} != {}'.format(correct_to,to))
        self.assertEqual(original_params, params, '"params" has been corrupted. {} != {}'.format(original_params, params))

    def test_resolve_params_raises_exception_with_non_dict_arg(self):
        """_resolve_params(to, params): Raises an InvalidRequestParameterStructureException when 'params' is not dict.
        """
        print(self.shortDescription())

        req = OneM2MRequest()

        params = [1,2,3]

        try:
            req._resolve_params(to=None, params=params)
        except InvalidRequestParameterStructureException as err:
            self.assertEqual(params.__class__.__name__, err.type)

    def test_create(self):
        pass
    
    # def test_one_m2m_async_create_request(self):
    #     """Async request test """
    #     print(self.shortDescription())

    #     async def run_test():
    #         try:
    #             one_m2m_req = OneM2MRequest()
    #             # await the couroutine.
    #             res = await one_m2m_req.create_async('http://www.google.com')
    #             self.assertTrue(True, 'Its true')
    #         except Exception as err:
    #             print(err)

    #     self.loop.run_until_complete(run_test())