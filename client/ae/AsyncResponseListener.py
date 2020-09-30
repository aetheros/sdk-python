#!/usr/bin/env python

import json, asyncio, threading

from aiohttp import web
from client.onem2m.OneM2MPrimitive import OneM2MPrimitive

from client.onem2m.http.OneM2MResponse import OneM2MResponse

class AsyncResponseListenerFactory():
    """Builds and returns a single instance of AsyncReponseListener.
    """

    # Reference to the private inner class.
    instance = None

    def __init__(self, host='0.0.0.0', port=8080):
        """ Initialize the singletone or return the existing instance.
        """

        if AsyncResponseListenerFactory.instance is None:
            AsyncResponseListenerFactory.instance = AsyncResponseListenerFactory.__AsyncResponseListener(host, port)
    
    def get_instance(self):
        """ Return the singleton instance.
        """

        return AsyncResponseListenerFactory.instance

    class __AsyncResponseListener(threading.Thread):
        """ An async http server that runs in its own thread.
        """

        # Refernce to the event loop that will execute the async tasks.
        loop = None
        _stop_event = threading.Event()

        # Defaults are set in the factory class constructor 
        def __init__(self, host, port):
            threading.Thread.__init__(self)
            # Server host and port.
            self.host = host
            self.port = port

            self.runner = None

            # RQI to callback function map.  This is where callbacks will be stored.
            self.rqi_cb_map = {}

        async def _init_async_response_server(self):
            """Build the async response server.
            """

            print('Starting async server on {}:{}'.format(self.host, self.port))

            # Initialize the server.
            server = web.Application()

            # @todo make routes configurable via params.
            server.add_routes([
                web.get('/', self._handler),
                web.post('/', self._handler),
                web.get('/{rqi}', self._handler),
                web.post('/{rqi}', self._handler)
                ])

            # Start the server.
            if self.runner is None:
                self.runner = web.AppRunner(server)
                await self.runner.setup()
                site = web.TCPSite(self.runner, self.host, self.port)
                await site.start()

        def run(self):
            """Starts the async response server in its own thread.
            """
            asyncio.set_event_loop(asyncio.new_event_loop())
            loop =  asyncio.get_event_loop()
            loop.create_task(self._init_async_response_server())
            loop.run_forever()

        def stop(self):
            print('Stopping async response server.')
            # if self.thread is not None:
            self._stop_event.set()
        
        def stopped(self):
            return self._stop_event.is_set()

            # Block blarg.
            # web.run_app(server, host=self.host, port=self.port)

        async def _handler(self, req):
            request_method = req.method
            request_id = req.headers[OneM2MPrimitive.X_M2M_RI]

            res = web.Response(content_type=OneM2MPrimitive.CONTENT_TYPE_JSON)

            if request_id in self.rqi_cb_map.keys():
                # Execute callback and pass it the req.
                await self.rqi_cb_map[request_id](req, res)
            else:
                # No handler has been registed for this request id.
                res.set_status(4004)

            return res

        def set_rqi_cb(self, rqi, cb):
            """Set the callback function for a specific rqi.

            Args:
                rqi (string): The request id.
                cb (function): The callback function.
            """
            self.rqi_cb_map[str(rqi)] = cb # Key must be string.

        def call_rqi_cb(self, rqi, res=None):
            """Execute the callback function for the specified rqi.

            Args:
                rqi (string): The request id.
                res (OneM2MResponse): The response from the CSE.
            """
            if res is None:
                self.rqi_cb_map[rqi]()
            else:
                # Enforce callback response type.
                if not isinstance(res, OneM2MResponse): 
                    raise InvalidAsyncResponseHandlerArgument('Async response callbacks can have no argument or an argument of type OneM2MResponse')

                self.rqi_cb_map[rqi](res)

        def get_rqi_cb(self, rqi):
            """Return the callback function of the specified rqi.
            """
            try:
                return self.rqi_cb_map[rqi]
            except KeyError as err:
                # @todo create custom error.
                print(err)

        def __str__(self):
            return json.dumps(self.rqi_cb_map)

class InvalidAsyncResponseHandlerArgument(Exception):
    """
    """
    def __init__(self, msg):
        self.message = msg