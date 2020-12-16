#!/usr/bin/env python

import unittest

# import sys, os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client.cse.CSE import CSE
from client.ae.AE import AE
from client.exceptions.InvalidArgumentException import InvalidArgumentException


class CSETests(unittest.TestCase):
    CSE = CSE('localhost', 8100)

    def test_registration_with_invalid_arg(self):
        """AE registration fails with non AE instance argument."""
        print(self.shortDescription())

        try:
            self.CSE.register_ae('blah')
        except InvalidArgumentException as err:
            self.assertTrue(True)