#!/usr/bin/env python

import unittest, json

from client.ae.AE import AE, MissingRequiredAttibuteError
from client.exceptions.InvalidArgumentException import InvalidArgumentException


class AETests(unittest.TestCase):
    """AE Tests
    """

    def test_json_string_deserialization(self):
        """AE constructor deserializes json string representation of AE object into AE object.
        """
        print(self.shortDescription())

        ae_json_str = '''{
            "ae": {
                "aei": "N_SB_AE_1",
                "api": "N_SB_AE_1",
                "apn": "N_SB_AE_1",
                "ct": "20200807T163821",
                "lbl": [
                    "token=2ba9bd41-4d0d-4901-9df2-86cab0eaea2d"
                ],
                "lt": "20200807T163821",
                "pi": "PN_CSE",
                "poa": [
                    "http://localhost:7000"
                ],
                "ri": "C5def67ad000190",
                "rn": "C5def67ad000190",
                "rr": true,
                "ty": 2
            }
        }'''

        ae = AE(ae_json_str)

        # Test object instantiation.
        self.assertIsInstance(ae, AE)
        # Test object content.
        self.assertDictEqual(ae.__dict__, json.loads(ae_json_str)['ae'])

    def test_ae_instantiation(self):
        """AE initializes from dict containing required AE parameters.
        """
        print(self.shortDescription())

        ae_params = {
            'api': 'N_SB_AE_1',
            'apn': 'N_SB_AE_1',
            'aei': 'N_SB_AE_1',
            'poa': ['http://localhost:7000'],
        }

        ae = AE(ae_params)

        # Test object instantiation.
        self.assertIsInstance(ae, AE)
        # Test object content.
        self.assertDictEqual(ae.__dict__, ae_params)

    def test_ae_instantiation_with_dict_containing_ae_member(self):
        """AE initializes from dict containing AE member.
        """
        print(self.shortDescription())

        ae_json_str = '''{
            "ae": {
                "aei": "N_SB_AE_1",
                "api": "N_SB_AE_1",
                "apn": "N_SB_AE_1",
                "ct": "20200807T163821",
                "lbl": [
                    "token=2ba9bd41-4d0d-4901-9df2-86cab0eaea2d"
                ],
                "lt": "20200807T163821",
                "pi": "PN_CSE",
                "poa": [
                    "http://localhost:7000"
                ],
                "ri": "C5def67ad000190",
                "rn": "C5def67ad000190",
                "rr": true,
                "ty": 2
            }
        }'''

        ae = AE(json.loads(ae_json_str))

        # Test object instantiation.
        self.assertIsInstance(ae, AE)
        # Test object content.
        self.assertDictEqual(ae.__dict__, json.loads(ae_json_str)['ae'])

    def test_raises_missing_required_attribute_error(self):
        """AE construction raises MissingRequiredAttibureError.
        """
        print(self.shortDescription())

        with self.assertRaises(MissingRequiredAttibuteError):
            ae = AE({})