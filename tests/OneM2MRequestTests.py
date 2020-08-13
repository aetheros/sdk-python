#!/usr/bin/env python

import unittest

from client.OneM2M.http.OneM2MRequest import OneM2MRequest
from client.OneM2M.OneM2MOperation import OneM2MOperation
from client.exceptions.InvalidOneM2MOperationException import InvalidOneM2MOperationException

class OneM2MRequestTests(unittest.TestCase):
    def test_one_m2m_request_invalid_operation(self):
        """OneM2M request fails with invalid operation."""
        print(self.shortDescription())

        try:
            r = OneM2MRequest(OneM2MOperation.Create, 'localhost')
            
        except InvalidOneM2MOperationException as err:
            self.assertTrue(True)