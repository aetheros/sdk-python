# Copyright (c) Aetheros, Inc.  See COPYRIGHT

#!/usr/bin/env python

import os, sys, json, time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client.onem2m.OneM2MPrimitive import OneM2MPrimitive
from client.cse.CSE import CSE
from client.ae.AE import AE


def main():
    try:
        AE_ID = '1234567890'

        # host, port, resource
        CSE_HOST = 'dev9.usw1.aws.corp.grid-net.com'
        CSE_PORT = 21300

        # Create an instance of CSE
        pn_cse = CSE(CSE_HOST, CSE_PORT)

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
        res.dump('Register AE')

        if res.rsc != OneM2MPrimitive.M2M_RSC_CREATED:
            print('Could not register AE\nExiting...')
            sys.exit()

        print('AE registration successful:')

        # Discover containers.
        print('Discovering containers:')
        containers = pn_cse.discover_resources()
        containers.dump('Discover Containers')

        print('Retrieved {} containers\n'.format(len(containers.pc['m2m:uril'])))
    except Exception as err:
        print('Exception raised...\n')
        print(err)
    finally:
        print('Cleaning up...')
        # Clean up AE.
        if pn_cse.ae is not None:
            del_res = pn_cse.delete_ae()
            del_res.dump('Delete AE')


if __name__ == '__main__':
    main()
