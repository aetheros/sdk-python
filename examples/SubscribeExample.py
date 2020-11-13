#!/usr/bin/env python

import os, sys, json, time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client.onem2m.OneM2MPrimitive import OneM2MPrimitive
from client.cse.CSE import CSE
from client.ae.AE import AE
from client.ae.AsyncResponseListener import AsyncResponseListenerFactory


def main():
    try:
        AE_ID = '1234567890'

        # host, port, resource
        CSE_HOST = 'dev9.usw1.aws.corp.grid-net.com'
        CSE_PORT = 21300
        CSE_RESOURCE = 'PN_CSE'

        # Create an instance of CSE
        pn_cse = CSE(CSE_HOST, CSE_PORT, CSE_RESOURCE)

        # Create an AE instance to register with the CSE.
        req_ae = AE(
            {
                AE.M2M_ATTR_APP_ID: 'N_SB_AE_1',
                AE.M2M_ATTR_APP_NAME: 'N_SB_AE_1',
                AE.M2M_ATTR_AE_ID: AE_ID,
                AE.M2M_ATTR_POINT_OF_ACCESS: ['http://localhost:7000'],
            }
        )

        print('Registering AE "{}" with CSE @ {}'.format(req_ae.aei, CSE_HOST))

        # Register ae
        res = pn_cse.register_ae(req_ae)

        if res.rsc != OneM2MPrimitive.M2M_RSC_CREATED:
            print('Could not register AE\nExiting...')
            sys.exit()

        print('AE registration successful:')
        print(res.pc)

        # Discover containers.
        print('Discovering containers:')
        containers = pn_cse.discover_containers()
        print('Retrieved {} containers\n'.format(len(containers)))

        # Pick a container resource to work with.
        containerUri = containers[0]

        # Create a subscription to the container.
        print('Subscribing to container: {}'.format(containerUri))
        sub_res = pn_cse.create_subscription(containerUri, 'localhost:8080')
        print(sub_res.rsc)
        print(sub_res.pc)

        # Get the request id to register with the async response handler.
        # @todo the AsyncResponseHandler should be a member of the AE class and should
        # intialize the handler when a response is recieved indicating that further async
        # responses are to be expected.
        request_id = sub_res.rqi

        # Callback that will be execute whenever an HTTP request is sent to localhost:8080
        # and X-M2M-RI header is set.  The handler functions should process the request and
        # return the appropiate http response orginator.
        # @todo AsyncResponseListener needs further refinement.  It should work with OneM2M primitives, not
        # HTTP messages directly.
        # Params are aiohttp request and response instance.
        # https://docs.aiohttp.org/en/stable/web_reference.html?highlight=Request#request-and-base-request
        # https://docs.aiohttp.org/en/stable/web_reference.html?highlight=Response#response-classes
        async def request_handler(req, res):
            #  Process request.
            if req.method == 'POST' or res.body_exists():
                # Do something with the posted data...
                print(await req.json())

                # Modify response.
                res.set_status(2000)
                res.text = 'Message recieved'

            return res

        handlerFactory = (
            AsyncResponseListenerFactory()
        )  # default is localhost on post 8080
        handler = handlerFactory.get_instance()
        handler.set_rqi_cb(
            request_id, request_handler
        )  # Map request id to corresponding handler function.
        handler.start()

    except Exception as err:
        print('Exception raised...\n')
        print(err)
    finally:
        print('Cleaning up...')
        # Clean up AE.
        if pn_cse.ae is not None:
            del_res = pn_cse.delete_ae()
            print('AE delete response code {}: '.format(del_res.rsc))


if __name__ == '__main__':
    main()
