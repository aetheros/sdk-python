import os, sys, json, time, re

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client.onem2m.OneM2MPrimitive import OneM2MPrimitive
from client.onem2m.OneM2MPrimitive import OneM2MPrimitive
from client.onem2m.http.OneM2MRequest import OneM2MRequest
from client.cse.CSE import CSE
from client.ae.AE import AE
from client.ae.AsyncResponseListener import AsyncResponseListenerFactory
from client.onem2m.OneM2MResource import OneM2MResource, OneM2MResourceContent

from aiohttp import web
from aiohttp.payload import Payload

NOTIFICATION_SERVER_IP = '0.0.0.0'
NOTIFICATION_SERVER_PORT = 44346

class LcoControlSchedule(OneM2MResource):
    def __init__(self, dict: OneM2MResourceContent):
        super().__init__('lco:lcocs', dict)

class LcoTelemetryTrigger(OneM2MResource):
    def __init__(self, dict: OneM2MResourceContent):
        super().__init__('lco:lcottr', dict)

class Lwm2mNotificationClassAttributes(OneM2MResource):
    def __init__(self, dict: OneM2MResourceContent):
        super().__init__('lwm2m:nca', dict)


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
        ae_id = 'C701b0da5000002'
        app_id = 'Nverizon-lco'
        ae_credential_id = 'EJ9CK1LAIL07FVHR'

        node = '/PN_CSE/nod-015322009906000'    # optional

        #TODO:
        poa = 'http://<AE public IP Address>:44346/notify'

        cse = CSE('api.netsense.aetheros.com', 443, 'PN_CSE')
        cse.transport_protocol = 'https'

        ae = cse.get_ae(ae_id) if ae_id else None

        if not ae:

            print('Registering new AE with {}'.format(app_id))

            ae_reg_response = cse.register_ae(
                AE(
                    {
                        OneM2MPrimitive.M2M_PARAM_APP_ID         :  app_id,
                        OneM2MPrimitive.M2M_PARAM_AE_ID          :  ae_credential_id,
                        OneM2MPrimitive.M2M_PARAM_POINT_OF_ACCESS: [poa],
                    }
                )
            )

            ae_reg_response.dump('Register AE')
            print('\n===============================\n')

        print('Using AE with ID {}'.format(cse.ae.aei))


        if not node:

            print('Discovering existing nodes')
            discover_response = cse.discover_containers()

            discover_response.dump('Discover AE')
            print('\n===============================\n')

            # Pick a random container.
            nodes = discover_response.pc['m2m:uril']
            node = next(x for x in nodes if re.match(r'.*/nod-[0-9]{15}$', x))

        print('Using node {}'.format(node))
        #retrieve_node_children = cse.retrieve_resource(node)

        #slot_value = 282694747447920
        slot_value = 282763500453888
        #slot_value = 352144368606240

        print('Updating Control Schedule')
        update_lcs_response = cse.update_resource(node + '/lcocs', LcoControlSchedule({
            'slots': [slot_value] * 42
        }))

        dump_response('Update Control Schedule', update_lcs_response)
        print('\n===============================\n')


        print('Writing Telemetry Trigger')
        update_lottr_response = cse.update_resource(node + '/lcottr', LcoTelemetryTrigger({
            'cloudActiveEnergy': int(time.time()) - 60 * 60 * 4   # 4 hours ago
        }))
        dump_response('Write Telemetry Trigger', update_lottr_response)
        print('\n===============================\n')


        print('Reading Telemetry Transmission')
        ttn_response = cse.retrieve_resource(node + '/lcottn0')
        ttn_response.dump('Read Telemetry Transmission')

        print('\n===============================\n')

        ttn = json.loads(ttn_response.pc['lco:lcottn']['data'])
        print('Active Energy:\n{}'.format(json.dumps(ttn, indent=2)))

        print('\n===============================\n')

        sub_name = 'illuminance-{}'.format(ae_id)
        lcoi_url = node + '/lcoi'

        print('Checking for subscriptions on {}'.format(lcoi_url))
        # retrieve_sub_response = cse.check_existing_subscriptions(lcoi_url)
        retrieve_sub_response = OneM2MRequest(
            cse.get_to(lcoi_url),
            {
                OneM2MPrimitive.M2M_PARAM_FROM: cse.ae.ri,
                OneM2MPrimitive.M2M_PARAM_FILTER_USAGE: OneM2MPrimitive.M2M_FILTER_USAGE.Discovery.value,
                OneM2MPrimitive.M2M_PARAM_RESOURCE_TYPE: OneM2MPrimitive.M2M_RESOURCE_TYPES.Subscription.value,
                OneM2MPrimitive.M2M_PARAM_RESOURCE_NAME: sub_name,
                #'poa': poa,
            },
        ).retrieve()
        retrieve_sub_response.dump('Discover Subscriptions')
        print('\n===============================\n')

        if "poa" in locals():

            existing_subscriptions = retrieve_sub_response.pc['m2m:uril']
            existing_subscription = None

            for sub in existing_subscriptions:

                sub_resource = cse.retrieve_resource(sub).pc['m2m:sub']

                if poa in sub_resource['nu']:
                    existing_subscription = sub
                else:
                    delete_sub_response = cse.delete_resource(sub)
                    delete_sub_response.dump('Delete Subscription')


            if not existing_subscription:
                print('\n===============================\n')
                print(
                    'Creating subscription {} subscriptions on {}'.format(
                        sub_name, lcoi_url
                    )
                )
                create_sub_response = cse.create_subscription(
                    lcoi_url, sub_name, poa,
                    result_content=OneM2MPrimitive.M2M_RESULT_CONTENT_TYPES.HierarchicalAddress.value,
                    event_types=[
                        OneM2MPrimitive.M2M_NOTIFICATION_EVENT_TYPES.UpdateOfResource.value,
                        OneM2MPrimitive.M2M_NOTIFICATION_EVENT_TYPES.CreateOfDirectChildResource.value,
                    ]
                )
                create_sub_response.dump('Create Subscription')
                print('\n===============================\n')

                existing_subscription = lcoi_url + '/' + sub_name


        print('\n===============================\n')
        print('Setting pmin/pmax on {}'.format(lcoi_url))

        nca_url = lcoi_url + '/nca'
        nca = Lwm2mNotificationClassAttributes({
            "minimumPeriod": 15,
            "maximumPeriod": 10 * 60,
        })

        try:
            update_nca_response = cse.update_resource(nca_url, nca)
            update_nca_response.dump('Update NCA')
            
        except Exception as e:
            create_nca_response = cse.create_resource(lcoi_url, 'nca', nca)
            create_nca_response.dump('Create NCA')

        print('\n===============================\n')


        # Create a callback function to handle async notifications from the sub.
        async def cb(req, res: web.Response):
            #  Process request.
            if req.method == 'POST' or req.body_exists():
                body = await req.json()
                print(body['m2m:sgn']['nev']['rep']['lco:lcoi'])

                # Modify response.  All that is set is content_type == OneM2MPrimitive.CONTENT_TYPE_JSON
                res.set_status(int(OneM2MPrimitive.M2M_RSC_OK))
                res.body = json.dumps({
                    "msg":"ok"
                    }
                ) # type: ignore

            # Send response.
            return res

        print('\n===============================\n')
        print('Starting async response server on http://{}:{}'.format(NOTIFICATION_SERVER_IP, NOTIFICATION_SERVER_PORT))
        print('\n===============================')
        print('POST requests to "http://{}:{}/notify" with header "X-M2M-RI: {}"'.format(NOTIFICATION_SERVER_IP, NOTIFICATION_SERVER_PORT, existing_subscription))
        print('===============================')
        async_response_handler = cse.ae.get_async_response_handler(NOTIFICATION_SERVER_IP, NOTIFICATION_SERVER_PORT)
        # Register callback to the sub rqi.
        async_response_handler.set_rqi_cb(existing_subscription, cb)
        async_response_handler.start()

        # Async handler runs in a daemon thread.  Keep the main process alive until ctrl-c.
        while True:
            pass

    except KeyboardInterrupt:
        print('\n===============================\n')
        print('Cleaning up...')
        print('\n===============================\n')
        print('Removing existing {} subscriptions on {}'.format(sub_name, container))
        for sub in retrieve_sub_response.pc['m2m:uril']:
            del_response = cse.delete_resource(sub)
            del_response.dump('Delete Subscription')

        # Clean up AE.
        if cse.ae is not None:
            del_res = cse.delete_ae()
            del_res.dump('Delete AE')


#    except Exception as e:
#        print(e)
#    finally:
#        pass

if __name__ == '__main__':
    main()