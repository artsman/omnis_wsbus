# -*- coding: utf-8 -*-
from asyncio import wait
from json import dumps
from weakref import WeakSet

from websockets import ConnectionClosed

from .app import app

# Bind the web socket tracking to the app
app['websockets'] = WeakSet()


def build_user_message():
    """
    :return: User payload in JSON format
    """
    return dumps({'type': 'users', 'count': len(app['websockets'])})


async def send_message(user, message):
    """
    Send a message, but suppress disconected messages.

    :param user: user (a.k.a websocket instance) to send from
    :param message: message to send
    """
    try:
        return await user.send(message)
    except ConnectionClosed:
        pass


async def relay_message(message, current_user=None):
    """
    Relay the given message to all users, except the current user (if given)

    :param message: Message to relay
    :param current_user: Current user web socket instance
    :return:
    """
    users = [
        send_message(user, message)
        for user in app['websockets']
        if user is not current_user
    ]
    if not users:
        return

    await wait(users)


async def notify_users():
    """
    Notify all users of the user state
    """
    if not app['websockets']:
        return

    message = build_user_message()
    await wait([user.send(message) for user in app['websockets']])


async def register(websocket):
    """
    Register a new websocket (a.k.a user) in the applications current websocket set

    :param websocket: websocket to register
    """
    app['websockets'].add(websocket)
    await notify_users()


async def unregister(websocket):
    """
    Unregister an existing websocket (a.k.a user) from the applications current websocket set

    :param websocket: websocket to unregister
    """
    app['websockets'].discard(websocket)
    await notify_users()


async def relay(websocket, path):
    """
    Count values in the web socket

    :param websocket: websocket to communicate on
    :param path: Path being used
    """
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    try:
        while True:
            try:
                message = await websocket.recv()
            except ConnectionClosed:
                break
            else:
                await relay_message(message, current_user=websocket)
    finally:
        await unregister(websocket)
