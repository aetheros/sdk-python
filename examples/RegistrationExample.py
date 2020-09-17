#!/usr/bin/env python

import os, sys, json, time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client.cse.CSE import CSE
from client.ae.AE import AE

def main():
    try:
        # Create an instance of PN_CSE
        cse = CSE('dev9.usw1.aws.corp.grid-net.com', 21300)

        # Create a request AE to send to the CSE.
        req_ae = AE({
            'api': 'N_SB_AE_1',
            'apn': 'N_SB_AE_1',
            'aei': 'N_SB_AE_1',
            'poa': ["http://localhost:7000"]
        })

        print('Register AE with CSE recieved')

        # Returns an instance of AE that will be used in all subsequent requests to the CSE.
        res_ae = cse.register_ae(req_ae)

        print('Response AE recieved')
        print(res_ae)

        print('\nSleeping for 3 seconds...\n')

        time.sleep(3)
        
        # Returns a list of container resources.
        print('Discovering containers')
        containers = cse.discover_containers(res_ae)
        print('Retrieved {} containers'.format(len(containers)))

        print('\nSleeping for 3 seconds...\n')
        time.sleep(3)

        rsc = containers[1]

        print('Retrieving resource: {}'.format(rsc))
        resource = cse.retrieve_resource(res_ae, rsc)

        print(resource)

        print('\nSleeping for 3 seconds...\n')

    except Exception as err:
        print('Exception raised...\n')
        print(err)
    finally:
        print('Cleaning up...')
        # Clean up AE.
        del_res = cse.delete_ae(res_ae)

        print(del_res)



if __name__ == '__main__':
    main()
