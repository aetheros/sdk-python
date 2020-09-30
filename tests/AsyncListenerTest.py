#!/usr/bin/env python

import unittest
import requests

from client.onem2m.http.OneM2MResponse import OneM2MResponse
# import sys, os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client.ae.AsyncResponseListener import AsyncResponseListenerFactory, InvalidAsyncResponseHandlerArgument

class AsyncResponseListenerTests(unittest.TestCase):
    def test_ae_response_listener_singleton(self):
        """AsyncResponseListernerFactory returns singleton instance of AsyncResponseListener."""
        print(self.shortDescription())

        f1 = AsyncResponseListenerFactory()
        i1 = id(f1.get_instance())

        f2 = AsyncResponseListenerFactory()
        i2 = id(f2.get_instance())


        self.assertEqual (i1, i2, 'Factory failed to return the same instance.')

    def test_enforce_callback_argument_datatype(self):
        """Response handler argument must be OneM2MResponse object."""
        print(self.shortDescription())

        # Instantiate the factory, get the singleton handler and start the server.
        f1 = AsyncResponseListenerFactory()
        i1 = f1.get_instance()
        i1.start()

        # Create an invalid request that should throw an exception.
        rqi = 123456
        oneM2MResponse = 'not a valid argument...'

        # Callback
        def cb():
            return 123
        

        try:
            # Set the callback.
            i1.set_rqi_cb(rqi, cb)

            # Execute the callback.
            self.assertEquals(123,i1.call_rqi_cb(rqi, oneM2MResponse), 'Invalid callback response')
        except InvalidAsyncResponseHandlerArgument as err:
                i1.stop()
                # Catch the exception.
                self.assertIsInstance(err, InvalidAsyncResponseHandlerArgument, 'Invalid async response handler argument.')

        # Create a valid request that should not throw an exception.
        rqi = 654321
        oneM2MResponse = OneM2MResponse(requests.Response())

        try:
            # Set the callback.
            self.assertEquals(123,i1.call_rqi_cb(rqi, oneM2MResponse), 'Invalid callback response')

            # Execute the callback.
            i1.call_rqi_cb(rqi, oneM2MResponse)
        except InvalidAsyncResponseHandlerArgument as err:
                # No exception should be raised.
                self.assertTrue(False, 'Invalid async response handler argument.')
        
    # def test_set_rqi_callback(self):
    #     l = AsyncResponseListenerFactory().get_instance()

    #     rqi = 123

    #     def cb(req):
    #         return req

    #     l.set_rqi_cb(rqi, cb)

    #     l.state_async_response_server()

    #     l.stop()


        