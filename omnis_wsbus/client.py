# -*- coding: utf-8 -*-
#
from datetime import datetime
from websockets import connect

async def listen(uri, ssl_context):
    async with connect(uri, ssl=ssl_context) as ws:
        while True:
            msg = await ws.recv()
            print(f'{datetime.now().isoformat()}: {msg}')
