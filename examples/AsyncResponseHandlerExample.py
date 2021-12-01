# Copyright (c) Aetheros, Inc.  See COPYRIGHT

#!/usr/bin/env python

import os, sys, json, time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client.ae.AsyncResponseListener import AsyncResponseListenerFactory
from client.onem2m.OneM2MPrimitive import OneM2MPrimitive

from aiohttp import web

f1 = AsyncResponseListenerFactory('10.250.10.122', 8080)
i = f1.get_instance()
i.start()

async def cb(req: web.Request, res: web.Response):
    #  Process request.
    if req.method == 'POST' or req.body_exists():
        print(await req.json())

        # Modify response.
        res.set_status(2000)
        res.text = 'Response body...'

    return res


# Register callback.
i.set_rqi_cb('123456789', cb)
