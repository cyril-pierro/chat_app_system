"""Consumer

This module is demonstrates how the operations
for connecting, accepting, sending and receiving
websocket operations

Attributes:
    chat_consumer_logger (object): Logger
    AUTH_URL (str): Account service url
    SUPPORT_URL (str): Support Service url
    resource (object): Resource definition for trace metrics
    jaeger_exporter (object): Jaeger Exportor for the trace metrics

"""
import json
from typing import Any, Optional
from urllib.parse import parse_qs

import requests
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from websocket.tools.log import Log

chat_consumer_logger = Log(__file__)
AUTH_URL = settings.AUTH_MANAGEMENT_URL
SUPPORT_URL = settings.SUPPORT_URL

resource = Resource(attributes={SERVICE_NAME: "chat.service"})

jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)

trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer_provider().get_tracer(__name__)

trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)  # type: ignore
)


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

    async def chat_bot_message(self, event: Any) -> None:
        """Chat Bot Stream

        This method is responsible for
        sending message to a group channel
        for chat support

        Args:
            event (object): event raised by the socket
        """
        message = event.get("message")
        user = event.get("user")
        await self.send(
            text_data=json.dumps(
                {"type": "chat_bot_message", "message": message, "user": user}
            )
        )

    async def chat_message(self, event: Any) -> None:
        """Chat Stream

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

        if self.get_room_name() == "support":
            support_message = await self.get_reply(message)
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "chat_bot_message",
                        "message": support_message,
                        "user": "Dave",
                    }
                )
            )
        else:
            await self.channel_layer.group_send(
                self._room_group_name,
                {"type": "chat_message", "message": message, "user": user},
            )

    @tracer.start_as_current_span("support-request-time")
    async def get_reply(self, message: str) -> str:
        """Send Message to AI model

        This method is used for maintaining a
        conversation with a user

        Args:
            message (str): Message sent by the user
        Returns
            str : Reply from the AI model
        """
        response = requests.post(
            f"{SUPPORT_URL}/api/v1/support", json={"question": message}
        )
        support_message = (
            response.json()["answer"]
            if response.status_code == 200
            else "Under Maintainance"
        )
        return support_message

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

    @tracer.start_as_current_span("auth-request-time")
    async def is_user_authenticated(self) -> Optional[bool]:
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
