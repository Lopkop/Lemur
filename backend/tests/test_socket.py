import json

import pytest

from backend.db.schemas import SignUpResponseModel, UserModel
from backend.sockets.connection_handler import ConnectionHandler
from backend.tests.mocks.socket_mock import SocketMock

test_requests = {"sign_up": r'{"user_name": "funky_goblin"}'}

test_user = UserModel(
    name="funky_goblin", user_id="a-user-id", chatroom_id="a-chatroom-id"
)

test_responses = {"sign_up": SignUpResponseModel(status=True, user=test_user).dict()}


@pytest.mark.asyncio
async def test_socket_accepts_connection():
    socket = SocketMock(test_requests["sign_up"])
    await socket.accept()

    assert socket.connection_accepted is True


@pytest.mark.asyncio
async def test_socket_can_process_accepted_connection_into_JSON_object():
    socket = SocketMock(test_requests["sign_up"])
    connection_handler = ConnectionHandler(socket)
    request = await connection_handler.get_request()

    expected_JSON = {"user_name": "funky_goblin"}

    assert request == expected_JSON


@pytest.mark.asyncio
async def test_socket_can_process_JSON_objects_and_send_them_():
    socket = SocketMock(json.dumps(test_responses["sign_up"]))
    connection_handler = ConnectionHandler(socket)
    await connection_handler.send_response(test_responses["sign_up"])

    expected_sent_response = r'{"status": true, "user": {"name": "funky_goblin", "user_id": "a-user-id", "chatroom_id": "a-chatroom-id"}}'

    assert socket.sent_response == expected_sent_response
