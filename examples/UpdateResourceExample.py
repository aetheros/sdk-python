#!/usr/bin/env python

import os, sys, json, time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client.onem2m.OneM2MPrimitive import OneM2MPrimitive
from client.onem2m.resource.Subscription import Subscription
from client.cse.CSE import CSE
from client.ae.AE import AE

def main():
    try:
        AE_ID = '1234567890'

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
            AE.M2M_ATTR_AE_ID: AE_ID,
            AE.M2M_ATTR_POINT_OF_ACCESS: ["http://localhost:7000"]
        })

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
        sub_res  = pn_cse.create_subscription(containerUri, '10.250.10.142:8080')
        print('Subscription created: '.format(sub_res.cn))

        print('Retrieving subscription: {}'.format(sub_res.cn))
        res = pn_cse.retrieve_resource(sub_res.cn)
        # Use the returned subscription resource as update target.
        res_sub_dict = json.loads(res.pc)['sub']

        update_sub_dict = {}
        # Strip non-updatable attributes.
        for k,v in res_sub_dict.items():
            if k not in('ct','lt','pi','ri','rn','ty'):
                update_sub_dict[k] = v

        
        sub = Subscription(update_sub_dict)
        print(sub)

        print('Updating subscription resource: {}'.format(sub_res.cn))
        sub.nu = ['0.0.0.0']
        res = pn_cse.update_resource(sub_res.cn, sub)
        print(json.loads(res.rsc))

        print('Retrieving subscription: {}'.format(sub_res.cn))
        res = pn_cse.retrieve_resource(sub_res.cn)
        print(json.loads(res.pc))

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
