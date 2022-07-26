from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from db.db import ChatRoomFactory, UserFactory
from src.sockets.connection_handler import ConnectionHandler

app = FastAPI()
# Instantiate DatabaseClient

user_factory = UserFactory()
chat_room_factory = ChatRoomFactory()


@app.websocket("/sign_up")
async def sign_up(websocket: WebSocket):
    """Signs Up New Users"""
    connection = ConnectionHandler(websocket)
    request = connection.get_request()
    user_obj = user_factory.create_user(request["name"])
    response = {
        "username": user_obj.name,
        "chat_room_id": user_obj.chat_room_id,
        "user_id": user_obj.id,
    }  # uses ResponseFactory to generate Response JSON from User Object
    await connection.send_response(response)


@app.websocket("/send_message/{chat_room_id}")
async def send_message(websocket: WebSocket, chat_room_id: str):
    """Sends Message to Given Chatroom | Broadcast to all users"""
    connection = ConnectionHandler(websocket)
    try:
        while True:
            request = await connection.get_request()
            message = request["message"]
            user_id = request["user_id"]
            item = chat_room_factory.create_messaage(chat_room_id, user_id, message)
            await connection.send_response(
                {"message": item.message, "user_id": item.user_id}
            )
    except WebSocketDisconnect:
        print("Websocket disconnect!")


@app.websocket("/get_messages/{chat_room_id}")
async def get_messages(websocket: WebSocket, chat_room_id: str):
    """Gets All Messages Of Given Chatroom"""
    connection = ConnectionHandler(websocket)
    request = await connection.get_request()
    page = request.get("page", 1)
    size = request.get("size", 20)
    messages = chat_room_factory.get_chat_room_messages(chat_room_id, page, size)
    for item in messages:
        await connection.send_response(
            {"message": item.message, "user_id": item.user_id}
        )
