from typing import Annotated

from fastapi import FastAPI, WebSocket, Depends, WebSocketDisconnect, HTTPException
from sqlalchemy.orm import scoped_session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware  # todo: later should be replaced

from sockets.connection_manager import ConnectionManager
from db.dbapi import DatabaseService
from db import schemas
from db.schemas import MessageModel
from sockets.response_factory import ResponseFactory
from utils import RandomIdGenerator, create_and_get_chatroom, hash_password

app = FastAPI()
db = DatabaseService()
response = ResponseFactory()
manager = ConnectionManager()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # can alter with time
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                session: scoped_session = Depends(db.get_db)):
    user = db.fetch_user_by_name(session, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username")
    hashed_password = hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect password")

    return {"access_token": user.name, "token_type": "bearer"}


@app.post("/sign-up", response_model=schemas.SignUpResponseModel)
async def sign_up(
        user: schemas.UserModel, session: scoped_session = Depends(db.get_db)
):
    """Signs Up New Users"""
    db.save_user(session, user)
    if db.fetch_user_by_name(session, user.name):
        return response.generate_sign_up_response(True, user)
    return response.generate_sign_up_response(False, user)


@app.post("/create-chat", response_model=schemas.ChatRoomModel | dict)
async def create_chat(
        user: schemas.UserModel, session: scoped_session = Depends(db.get_db)
):
    """Create chatroom and save to db"""
    if not db.fetch_user_by_name(session, user.name):
        return response.generate_user_undefined_error_response(user)

    generate_id = RandomIdGenerator()
    chatroom_name = generate_id(chatroom_name=True)
    chat = create_and_get_chatroom(user, name=chatroom_name)
    db.save_chatroom(session, chat)

    if db.fetch_chat_by_name(session, chatroom_name):
        return response.generate_chat_response(True, chat)
    return response.generate_chat_response(False, chat)


@app.post("/connect-to-chat")
async def connect_to_chat(
        chat: schemas.ChatRoomModel, session: scoped_session = Depends(db.get_db)
):
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


@app.websocket("/{chatroom}/{username}")
async def websocket_endpoint(
        websocket: WebSocket,
        username: str,
        chatroom: str,
        session: scoped_session = Depends(db.get_db),
):
    await manager.connect(chatroom, username, websocket)

    try:
        while True:
            text = await websocket.receive_text()
            message = MessageModel(text=text, user=username)
            db.save_message(session, chatroom, message)

            await manager.send_message(chatroom, message.json())
            print(f'{username} sent "{text}" to {chatroom}')  # need to log, not print

    except WebSocketDisconnect:
        manager.disconnect(chatroom, username)
