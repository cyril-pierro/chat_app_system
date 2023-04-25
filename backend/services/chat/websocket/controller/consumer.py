"""Consumer 

This module is demonstrates how the operations
for connecting, accepting, sending and receiving
websocket operations

Attributes:
    chat_consumer_logger (object): Logger
    AUTH_URL (str): Account service url

"""
import json
from urllib.parse import parse_qs

import requests
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from typing import Any, Union

from websocket.tools.log import Log

chat_consumer_logger = Log(__file__)
AUTH_URL = settings.AUTH_MANAGEMENT_URL


class ChatConsumer(AsyncWebsocketConsumer):
    """Chat Consumer Process

    This class is responsible for performing
    connect, accept, sending and receiving
    messages or websocket. It also authenticates
    a user who wants to connect.
    """
    _room_group_name = "default_group"
    _room_name = "default_name"

    async def connect(self) -> None:
        """Connect

        This method is responsible for allowing
        connections to the websocket
        """
        if await self.is_user_authenticated():
            # accept the connection
            await self.accept()
            # extract the chat room name from route
            self._room_name = self.get_room_name()
            # create a group name
            self._room_group_name = f"chat_app_{self._room_name}"

            # add a channel layer to add a group name
            await self.channel_layer.group_add(
                self._room_group_name, self.channel_name  # type: ignore
            )

            # send a message to the group when they are connected
            await self.channel_layer.group_send(
                self._room_group_name,
                # message to send to group
                {
                    # function name to send message
                    "type": "connection_established",
                    "message": "You are now connected",
                },
            )

    async def connection_established(self, event: Any) -> None:
        """Connection established

        This connection is responsible for 
        sending a success message when you are
        authenticated to the system

        Args:
            event (object): event raised by the socket
        """
        message = event.get("message")
        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "username": str(self.scope.get("user")),
                    "type": "start",
                }
            )
        )

    async def chat_message(self, event: Any) -> None:
        """Chat Message

        This method is responsible for 
        sending message to a group channel

        Args:
            event (object): event raised by the socket
        """
        message = event.get("message")
        user = event.get("user")
        await self.send(
            text_data=json.dumps(
                {"type": "chat_message", "message": message, "user": user}
            )
        )

    async def receive(self, text_data: str) -> None:
        """Receive

        This method is responsible for 
        receiving messages from a group channel

        Args:
            text_data (str): data sent through the channel
        """
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message")
        user = text_data_json.get("user")

        await self.channel_layer.group_send(
            self._room_group_name,
            {"type": "chat_message", "message": message, "user": user},
        )

    async def disconnect(self, close_code=None):
        """Disconnect from websocket

        This method is responsible for disconnecting
        a user from a socket

        Args:
            close_code

        Raises:
            AttributeError
        """
        try:
            # discard a group name
            await self.channel_layer.group_discard(
                self._room_group_name, self.channel_name
            )
        except AttributeError as exc:
            chat_consumer_logger.exception(exc.args[0])

    async def is_user_authenticated(self) -> Union[bool, None]:
        """User is authenticated

        This method is responsible for 
        authenticating a user before joining
        a channel

        Returns:
            bool: True is successful, False otherwise
        """
        query_string = self.scope["query_string"].decode("utf-8")
        params = parse_qs(query_string)
        token_key = params.get("token")[0]
        headers = {
            "Authorization": f"Bearer {token_key}",
            "Content-type": "application/json",
        }
        response = requests.get(f"{AUTH_URL}/api/v1/username", headers=headers)
        if response.status_code == 200:
            self.scope["user"] = response.json()["message"]
            return True
        await self.disconnect()

    def get_room_name(self):
        """Get the room name 

        Returns:
            str: the room name
        """
        route = self.scope.get("url_route")
        keywords = route.get("kwargs")
        room_name = keywords.get("room_name")
        return room_name
