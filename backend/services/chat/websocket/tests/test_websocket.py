"""Test Websocket

This module demonstrate the operations to test
websocket connection
"""
from unittest.mock import Mock, patch

import pytest

from ..utils.run import async_return

CUSTOMER_MODULE_LOC = "websocket.controller.consumer.ChatConsumer"


@pytest.mark.asyncio
async def test_websocket_connect(websocket_instance):
    websocket = await websocket_instance
    with patch(
        f"{CUSTOMER_MODULE_LOC}.is_user_authenticated",
        return_value=async_return(True),
    ):
        connected, _ = await websocket.connect()
        assert connected


@pytest.mark.asyncio
async def test_websocket_connection_message(websocket_instance):
    websocket = await websocket_instance

    with patch(
        f"{CUSTOMER_MODULE_LOC}.get_room_name",
        return_value="test_group_name",
    ):
        with patch(
            f"{CUSTOMER_MODULE_LOC}.is_user_authenticated",
            return_value=async_return(True),
        ):
            _, _ = await websocket.connect()
            response = await websocket.receive_json_from()
            assert response.get("type") == "start"
            assert response.get("message") == "You are now connected"


@pytest.mark.asyncio
async def test_websocket_send_and_recieve(websocket_instance):
    websocket = await websocket_instance

    with patch("websocket.controller.consumer.requests.get") as mock_request:
        mock_response = Mock()
        mock_request.return_value = mock_response
        mock_response.json.return_value = {"message": "test_user"}
        mock_response.status_code = 200
        with patch(f"{CUSTOMER_MODULE_LOC}.get_room_name", return_value="ghana"):
            _, _ = await websocket.connect()
            # skip connection message
            _ = await websocket.receive_json_from()
            await websocket.send_json_to(
                {"message": "hello there", "user": "test_user"}
            )
            response = await websocket.receive_json_from()
            assert response == {
                "type": "chat_message",
                "message": "hello there",
                "user": "test_user",
            }

            await websocket.disconnect()


@pytest.mark.asyncio
async def test_websocket_disconnect(websocket_instance):
    websocket = await websocket_instance
    await websocket.disconnect()
    assert await websocket.receive_nothing()

