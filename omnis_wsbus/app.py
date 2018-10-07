# -*- coding: utf-8 -*-
from _weakrefset import WeakSet

import aiohttp_jinja2

from aiohttp.web import Application, Response, RouteTableDef, WSMsgType, WebSocketResponse
from jinja2 import FileSystemLoader

from .frozen import resource_path


# App w/ Jinja2 templates
app = Application()
aiohttp_jinja2.setup(app, loader=FileSystemLoader(resource_path('templates')))

# Routes
routes = RouteTableDef()

@routes.get('/')
@aiohttp_jinja2.template('index.html')
async def hello(request):
    # Get the ports used for this server (the status_port) and the socket server (the socket_port)
    socket_port = app.get('socket_port', None)
    status_port = app.get('status_port', None)

    # Use the same IP that the user came in on, but replace the port
    host = request.host
    host = host.replace(str(status_port), str(socket_port))

    return {"host": host}


@routes.get('/stream')
async def stream(request):
    """
    Web socket stream for
    """
    ws_current = WebSocketResponse()
    ws_ready = ws_current.can_prepare(request)
    if not ws_ready.ok:
        return ws_current

    await ws_current.prepare(request)

    if 'websockets' not in request.app:
        request.app['websockets'] = WeakSet()

    request.app['websockets'].add(ws_current)

    while True:
        msg = await ws_current.receive()

        if msg.type == WSMsgType.text:
            for ws in request.app['websockets']:
                if ws is ws_current:
                    continue

                await ws.send_str(msg.data)
        elif msg.type == WSMsgType.BINARY:
            for ws in request.app['websockets']:
                if ws is ws_current:
                    continue

                await ws.send_bytes(msg.data)
        else:
            break

    request.app['websockets'].discard(ws_current)
    return ws_current

app.add_routes(routes)
