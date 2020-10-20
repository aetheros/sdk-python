
import os, sys, json, time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client.onem2m.OneM2MPrimitive import OneM2MPrimitive
from client.cse.CSE import CSE
from client.ae.AE import AE
from client.ae.AsyncResponseListener import AsyncResponseListenerFactory

NOTIFICATION_SERVER_IP = '10.250.10.121'
NOTIFICATION_SERVER_PORT = 8080

#
# Work flow:
#  1) Attempt to register AE with unregistered originator.
#  2) Register AE with originator.
#  3) Discover container nodes.
#  4) Retrieve a container node.
#  5) Check subscriptions to node.
#  6) Create subscription to node.
#  7) Handle async notifications from subscription.
#
def main():
    try:
        # Credentials from UI registration process.
        app_id = 'N_SB_AE_2'
        ae_credential_id = '5LKNUGX7OV27BMMR'

        print('Registering new AE with {}'.format(app_id))

        cse = CSE('dev9.usw1.aws.corp.grid-net.com', 21300, 'PN_CSE')
            
        ae_reg_response = cse.register_ae(
            AE({
                OneM2MPrimitive.M2M_PARAM_APP_ID: app_id,
                OneM2MPrimitive.M2M_PARAM_AE_ID: ae_credential_id,
                OneM2MPrimitive.M2M_PARAM_POINT_OF_ACCESS: ['{}:{}'.format(NOTIFICATION_SERVER_IP, NOTIFICATION_SERVER_PORT)]
            })
        )

        print('Response code: {}'.format(ae_reg_response.rsc))
        print('Response body:\n{}'.format(ae_reg_response.pc))
        print('\n===============================\n')

        print('Discovering existing nodes')
        discover_response = cse.discover_containers()
        print('Response code: {}'.format(discover_response.rsc))
        print('Response body:\n{}'.format(discover_response.pc))
        print('\n===============================\n')

        # Pick a random container.
        container = json.loads(discover_response.pc)['uril'][0]

        print('Using container {}'.format(container))
        create_sub_response = cse.retrieve_resource(container)
        print('Response code: {}'.format(create_sub_response.rsc))
        print('Response body:\n{}'.format(create_sub_response.pc))
        
        sub_name = 'sbabb-test-sub-1'

        print('\n===============================\n')
        print('Creating subscription {} subscriptions on {}'.format(sub_name, container))
        create_sub_response = cse.create_subscription(container, sub_name, '/notify')
        print('Response code: {}'.format(create_sub_response.rsc))
        print('Request ID: {}'.format(create_sub_response.rqi))
        print('Response body:\n{}'.format(create_sub_response.pc))

        print('\n===============================\n')
        print('Checking for subscriptions on {}'.format(container))
        retrieve_sub_response = cse.check_existing_subscriptions(container)
        print('Response code: {}'.format(retrieve_sub_response.rsc))
        print('Response body:\n{}'.format(retrieve_sub_response.pc))

        print('\n===============================\n')
        print('Starting async response server on http://{}:{}'.format(NOTIFICATION_SERVER_IP, NOTIFICATION_SERVER_PORT))
        print('\n===============================')
        print('POST requests to "http://{}:{}/notify" with header "X-M2M-RI: {}"'.format(NOTIFICATION_SERVER_IP, NOTIFICATION_SERVER_PORT, create_sub_response.rqi))
        print('===============================')
        async_response_handler = cse.ae.get_async_response_handler(NOTIFICATION_SERVER_IP, NOTIFICATION_SERVER_PORT)
        async_response_handler.start()

        # Create a callback function to handle async notifications from the sub.
        async def cb(req, res):
            #  Process request.
            if req.method == 'POST' or req.body_exists():
                print(await req.json())

                # Modify response.  All that is set is content_type == OneM2MPrimitive.CONTENT_TYPE_JSON
                res.set_status(OneM2MPrimitive.M2M_RSC_OK)
                res.body = json.dumps({
                    "msg":"ok"
                    }
                )

            # Send response.
            return res

        # Register callback to the sub rqi.
        async_response_handler.set_rqi_cb(create_sub_response.rqi, cb)

        # Async handler runs in a daemon thread.  Keep the main process alive until ctrl-c.
        while(True):
            pass

    except KeyboardInterrupt:
        print('\n===============================\n')
        print('Cleaning up...')
        print('\n===============================\n')
        print('Removing existing {} subscriptions on {}'.format(sub_name, container))
        for sub in json.loads(retrieve_sub_response.pc)['uril']:
            del_response  = cse.delete_resource(sub)
            print('Response code: {}'.format(del_response.rsc))
            print('Response body:\n{}'.format(del_response.pc))

        # Clean up AE.
        if cse.ae is not None:
            del_res = cse.delete_ae()
            print('AE delete response code: {} '.format(del_res.rsc))
    except Exception as e:
        print(e)
    finally:
        pass

if __name__ == '__main__':
    main()