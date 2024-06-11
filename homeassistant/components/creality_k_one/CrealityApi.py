"""Module to define the CrealityApi class for interacting with Creality printers."""

import asyncio
import json
import logging

from aiohttp import ClientSession, WSMsgType

logger = logging.getLogger(__name__)


class CrealityApi:
    """Class for interacting with Creality printers via WebSocket."""

    def __init__(self, uri):
        """Initialize the CrealityApi instance.

        :param uri: The URI of the WebSocket server.
        """
        self.uri = uri
        self.session = None
        self.ws = None
        self.callbacks = []
        self.listen_task = None

    async def connect(self):
        """Connect to the WebSocket server."""
        self.session = ClientSession()
        self.ws = await self.session.ws_connect(self.uri)
        self.listen_task = asyncio.create_task(self.listen())
        # Store a reference to the task if needed
        # self.listen_task = task

    async def close(self):
        """Close the WebSocket connection."""
        if self.ws:
            await self.ws.close()
        if self.session:
            await self.session.close()

    def register_callback(self, callback):
        """Register a callback function to handle received data.

        :param callback: The callback function to register.
        """
        self.callbacks.append(callback)

    def unregister_callback(self, callback):
        """Unregister a callback function.

        :param callback: The callback function to unregister.
        """
        if callback in self.callbacks:
            self.callbacks.remove(callback)

    async def listen(self):
        """Listen for incoming messages from the WebSocket server."""
        async for msg in self.ws:
            if msg.type == WSMsgType.TEXT:
                await self.update_data(msg.data)
            elif msg.type == WSMsgType.ERROR:
                logger.error(
                    "WebSocket connection closed with exception: %s",
                    self.ws.exception(),
                )
                break

    async def update_data(self, websocket_data):
        """Update data received from the WebSocket server.

        :param websocket_data: JSON data received from the WebSocket server.
        """
        try:
            json_data = json.loads(websocket_data)
            for callback in self.callbacks:
                await callback(json_data)

        except json.JSONDecodeError as e:
            logger.error("Received invalid json: %s", e)

    async def send_message(self, message):
        """Send a message to the WebSocket server.

        :param message: The message to send as a dictionary.
        """
        if self.ws:
            await self.ws.send_json(message)
