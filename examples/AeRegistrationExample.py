#!/usr/bin/env python

import os, sys, json, time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client.cse.CSE import CSE
from client.ae.AE import AE

def main():
    try:
        # host, port, resource
        CSE_HOST = 'dev9.usw1.aws.corp.grid-net.com'
        CSE_PORT = 21300
        CSE_RESOURCE = 'PN_CSE'

        # Create an instance of CSE
        pn_cse = CSE(
            CSE_HOST,
            CSE_PORT,
            CSE_RESOURCE
        )

        # Create an AE instance to register with the CSE.
        req_ae = AE({
            AE.M2M_ATTR_APP_ID: 'N_SB_AE_1',
            AE.M2M_ATTR_APP_NAME: 'N_SB_AE_1',
            AE.M2M_ATTR_AE_ID: 'N_SB_AE_1',
            AE.M2M_ATTR_POINT_OF_ACCESS: ["http://localhost:7000"]
        })

        print('Registering AE "{}" with CSE @ {}'.format(req_ae.aei, CSE_HOST))

        # Register ae 
        ae = pn_cse.register_ae(req_ae)

        # None indicates failed registration.
        if ae is None:
            print('Could not register AE\nExiting...')
            sys.exit()

        print('AE registration successful:')
        print(ae)

        # Discover containers.
        print('Discovering containers:')
        containers = pn_cse.discover_containers()
        print('Retrieved {} containers\n'.format(len(containers)))

        # Pick a container resource to work with.
        containerUri = containers[0]

        # Create a subscription to the container.
        print('Subscribing to container: {}'.format(containerUri))
        sub_res  = pn_cse.create_subscription(containerUri, '10.250.10.142:8080')
        print('Subscription created: '.format(sub_res.cn))

        print('Creating content instance of resource {}'.format(containerUri))
        cin_uri= pn_cse.create_content_instance(containerUri)
        print('Content instance created: '.format(cin_uri))

        print('Retrieving content instance: {}'.format(cin_uri))
        res = pn_cse.retrieve_content_instance(cin_uri)
        print(res)

        print('Retrieving subscription: {}'.format(sub_res.cn))
        res = pn_cse.retrieve_resource(sub_res.cn)
        print(json.loads(res.pc))

        print('Updating subscription resource: {}'.format(sub_res.cn))
        res = pn_cse.update_resource(sub_res.cn, 'sub', 'enc',
        "{'enc': { 'net': [4], 'ty': 5 }, 'nct': 1, 'nu': [notification_uri]}"
        )
        print(res)

        print('Retrieving subscription: {}'.format(sub_res.cn))
        res = pn_cse.retrieve_resource(sub_res.cn)
        print(json.loads(res.pc))

        # print('Retrieving container: {}'.format(containerUri))
        # res = pn_cse.retrieve_resource(containerUri)
        # print(json.loads(res.pc))

        # print('Retrieving most recent content instance: {}'.format(containerUri))
        # cin= pn_cse.retrieve_latest_content_instance(containerUri)

        # if cin is not None:
        #     print('Content instance recieved.')
        #     print(cin)
        # else:
        #     print('Could not latest retrieve content instance for resource: {}'.format(containerUri))

    except Exception as err:
        print('Exception raised...\n')
        print(err)
    finally:
        print('Cleaning up...')
        # Clean up AE.
        if pn_cse.ae is not None:
            del_res = pn_cse.delete_ae()
            print('AE delete response code: '.format(del_res.rsc))

if __name__ == '__main__':
    main()
