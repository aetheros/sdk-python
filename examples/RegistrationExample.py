#!/usr/bin/env python

import os, sys, json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client.cse.CSE import CSE
from client.ae.AE import AE

def main():
    cse = CSE('dev9.usw1.aws.corp.grid-net.com', 21300)

    # Create a request AE to send to the CSE.
    req_ae = AE({
        'api': 'N_SB_AE_1',
        'apn': 'N_SB_AE_1',
        'aei': 'N_SB_AE_1',
        'poa': ["http://localhost:7000"]
    })

    # Returns an instance of AE.
    res_ae = cse.register_ae(req_ae)

    print(res_ae)

if __name__ == '__main__':
    main()