"""Configuration for test

This module shows the configuration
done before you run a test

"""
import pytest
from channels.testing import WebsocketCommunicator
from websocket.controller import consumer


@pytest.fixture
@pytest.mark.asyncio
async def websocket_instance():
    test_token = "ghana"
    communicator = WebsocketCommunicator(
        consumer.ChatConsumer.as_asgi(), f"/ws/chat/ghana/?token={test_token}"
    )
    return communicator


@pytest.fixture
@pytest.mark.asyncio
async def websocket_support_instance():
    test_token = "ghana"
    support_comm = WebsocketCommunicator(
        consumer.ChatConsumer.as_asgi(), f"/ws/chat/support/?token={test_token}"
    )
    return support_comm
