#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from click import INT, STRING, group, option, argument, version_option, echo

from .constants import VERSION

@group()
@version_option(version=VERSION)
def main():
    """
    Main command group.  Using groups in anticipation of future options.
    """

@main.command()
@option('--socket-port', type=INT, default=6789, help="Port for WebSocket use")
@option('--status-port', type=INT, default=6790, help="Port for HTTP (Status page) use")
@option('--cert', type=STRING, default=None, help="Path to TLS/SSL public certificate")
@option('--key', type=STRING, default=None, help="Path to TLS/SSL private key")
@option('--dhparam', type=STRING, default=None, help="Path to TLS/SSL Diffie-Hellman parameter")
def run(socket_port=None, status_port=None, cert=None, key=None, dhparam=None):
    """
    Run the server.  The server always runs with TLS/SSL enabled.  Self-signed certificates
    are included by default and must be trusted by your operating system and browser before use.
    """
    import websockets

    from aiohttp.web import run_app
    from asyncio import get_event_loop
    from ssl import SSLContext, PROTOCOL_TLS_SERVER

    from .app import app
    from .frozen import is_frozen, resource_path
    from .sockets import relay

    # Set ports
    app['socket_port'] = socket_port
    app['status_port'] = status_port

    # Load SSL Certificate
    if cert is not None:
        cert = os.path.realpath(cert)
    else:
        cert = resource_path('ssl/server.crt')
        if not os.path.exists(cert):
            echo("Internal self-signed public certificate has not been generated.  Please "
                 "run `./build_ca_cert` followed by `./build_self_cert`.")

    if key is not None:
        key = os.path.realpath(key)
    else:
        key = resource_path('ssl/server.key')
        if not os.path.exists(key):
            echo("Internal self-signed private key has not been generated.  Please "
                 "run `./build_ca_cert` followed by `./build_self_cert`.")

    if dhparam is not None:
        dhparam = os.path.realpath(dhparam)
    else:
        dhparam = resource_path('ssl/dhparam.pem')
        if not os.path.exists(key):
            echo("Internal Diffie-Hellman parameter has not been generated.  Please "
                 "run `./build_ca_cert` followed by `./build_self_cert`.")

    if not os.path.exists(cert):
        echo(u"Unable to locate certificate: ", cert)

    if not os.path.exists(key):
        echo(u"Unable to locate key: ", cert)

    ssl_context = SSLContext(PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(cert, key)
    ssl_context.load_dh_params(dhparam)

    # Start event loop
    loop = get_event_loop()
    loop.run_until_complete(websockets.serve(relay, 'localhost', socket_port, ssl=ssl_context))
    loop.call_soon(lambda: print(f"======== WebSockets on https://0.0.0.0:{socket_port} ========"))

    run_app(app, port=status_port, ssl_context=ssl_context)


@main.command()
@option('--url', type=STRING, default='wss://127.0.0.1:6789', help="WebSocket URL to connect")
@option('--cafile', type=STRING, default=None, help="Path to CA file to trust for TLS/SSL (wss://) connections")
def watch(url=None, cafile=None):
    """
    Watch a web socket and dump all received content to stdout
    """
    from asyncio import get_event_loop
    from ssl import SSLContext, PROTOCOL_TLS_CLIENT

    from .client import listen
    from .frozen import resource_path

    if cafile is None:
        cafile = resource_path('ssl_root/root.crt')
        if not os.path.exists(cafile):
            echo("Internal self-signed root CA certificate has not been generated.  Please "
                 "run `./build_ca_cert` followed by `./build_self_cert`.")

    # Load SSL
    ssl_context = SSLContext(PROTOCOL_TLS_CLIENT)
    ssl_context.load_verify_locations(cafile=cafile)

    # Run listener
    loop = get_event_loop()
    loop.call_soon(lambda: print(f"Listening to {url}..."))
    loop.run_until_complete(listen(url, ssl_context))


@main.command()
@argument('path', type=STRING)
def certs(path):
    """
    Dump the bundled public SSL certificates used with the internal server
    """
    import shutil
    from .frozen import resource_path

    cert_path = os.path.join(path, 'server.crt')
    shutil.copyfile(resource_path('ssl/server.crt'), cert_path)
    echo(cert_path)
    root_path = os.path.join(path, 'root.crt')
    shutil.copyfile(resource_path('ssl_root/root.crt'), root_path)
    echo(root_path)
    echo('Done!')
