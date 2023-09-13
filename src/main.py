from datetime import datetime
from typing import Union

from fastapi import FastAPI, WebSocket, Depends, WebSocketDisconnect
from sqlalchemy.orm import scoped_session

from sockets.connection_manager import ConnectionManager
from db.dbapi import DatabaseService
from db import schemas
from db.schemas import MessageModel
from sockets.response_factory import ResponseFactory
from utils import RandomIdGenerator, create_and_get_chatroom, create_and_get_message

app = FastAPI()
db = DatabaseService()
response = ResponseFactory()
manager = ConnectionManager()

# todo: later should be replaced
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # can alter with time
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# время через которое будет удаляться чат; время жизни чата и юзер тоже должен удаляться

@app.post("/sign-up", response_model=schemas.SignUpResponseModel)
async def sign_up(user: schemas.UserModel, session: scoped_session = Depends(db.get_db)):
    """Signs Up New Users"""
    # todo: check if user is already signed in
    db.save_user(session, user)
    if db.fetch_user_by_name(session, user.name):
        return response.generate_sign_up_response(True, user)
    return response.generate_sign_up_response(False, user)


@app.post("/create-chat", response_model=Union[schemas.ChatRoomModel, dict])
async def create_chat(user: schemas.UserModel, session: scoped_session = Depends(db.get_db)):
    """Create chatroom and save to db"""
    if not db.fetch_user_by_name(session, user.name):
        return response.generate_user_undefined_error_response(user)

    generate_id = RandomIdGenerator()
    chatroom_name = generate_id()
    chat = create_and_get_chatroom(user, name=chatroom_name)
    db.save_chatroom(session, chat)

    if db.fetch_chat_by_name(session, chatroom_name):
        return response.generate_chat_response(True, chat)
    return response.generate_chat_response(False, chat)


@app.post('/connect-to-chat')
async def connect_to_chat(chat: schemas.ChatRoomModel, session: scoped_session = Depends(db.get_db)):
    """Connects user to chatroom"""
    user = chat.users[0]
    messages = db.fetch_chatroom_messages(session, chat.name)
    chat.messages = messages
    if not (user_db := db.fetch_user_by_name(session, user.name)):
        return response.generate_user_undefined_error_response(user)
    if not db.fetch_chat_by_name(session, chat.name):
        return response.generate_chat_response(status=False, chatroom=chat)
    db.add_user_to_chatroom(session, chatroom_model=chat, user_model=user)

    if user_db in db.fetch_chat_by_name(session, chat.name).users:
        return response.generate_chat_response(status=True, chatroom=chat)
    return response.generate_chat_response(status=False, chatroom=chat)


@app.websocket("/ws/{chatroom}/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str, chatroom: str,
                             session: scoped_session = Depends(db.get_db)):
    await manager.connect(chatroom, username, websocket)

    try:
        while True:
            text = await websocket.receive_text()
            message = MessageModel(text=text, user=username)
            db.save_message(session, chatroom, message)

            await manager.send_message(chatroom, message.json())
            print(f'{username} sent "{text}" to {chatroom}') # need to log, not print

    except WebSocketDisconnect:
        manager.disconnect(chatroom, username)
