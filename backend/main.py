from datetime import datetime, timedelta

from fastapi import FastAPI, WebSocket, Depends, WebSocketDisconnect, HTTPException, status, Response
from sqlalchemy.orm import scoped_session
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware  # todo: later should be replaced

from sockets.connection_manager import ConnectionManager
from db.dbapi import DatabaseService
from db import schemas
from db.schemas import MessageModel
from sockets.response_factory import ResponseFactory
from utils import RandomIdGenerator, create_and_get_chatroom
from security import authenticate_user, create_access_token

app = FastAPI()
db = DatabaseService()
response_factory = ResponseFactory()
manager = ConnectionManager()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/login", response_model=schemas.SignUpResponseModel)
async def login(user: schemas.UserModel, response: Response,
                session: scoped_session = Depends(db.get_db)):
    user = authenticate_user(session, user.name, user.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = db.fetch_token_by_username(session, user.name)
    response.set_cookie(key="access_token", value=f"Bearer {access_token.token}", httponly=True)
    response.body = 201
    return response_factory.generate_sign_up_response(201, access_token.token)


@app.post("/sign-up", response_model=schemas.SignUpResponseModel)
async def sign_up(user: schemas.UserModel, response: Response,
                  session: scoped_session = Depends(db.get_db)):
    if db.fetch_user_by_name(session, user.name):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User with this name already exists',
            headers={"WWW-Authenticate": "Bearer"},
        )

    current_time = datetime.now()
    expires_delta = timedelta(hours=user.lifetime)
    expiration_time = current_time + expires_delta
    user.lifetime = expiration_time

    db.save_user(session, user)
    access_token = create_access_token({"name": user.name})
    db.save_token(session, access_token, expiration_time, user.name)

    response.set_cookie(key="access_token", value=f"Bearer {access_token[0]}", httponly=True)
    return response_factory.generate_sign_up_response(201, access_token)


@app.get('/get_user')
async def get_user(access_token: str, session: scoped_session = Depends(db.get_db)):
    user = db.fetch_user_by_access_token(session, access_token)
    if not db.fetch_user_by_name(session, user.name):
        return response_factory.generate_user_undefined_error_response(user)
    return user


@app.post("/create-chat", response_model=schemas.ChatRoomModel | dict)
async def create_chat(
        user: schemas.UserModel, session: scoped_session = Depends(db.get_db)
):
    """Create chatroom and save to db"""
    if not db.fetch_user_by_name(session, user.name):
        return response_factory.generate_user_undefined_error_response(user)

    generate_id = RandomIdGenerator()
    chatroom_name = generate_id(chatroom_name=True)
    chat = create_and_get_chatroom(user, name=chatroom_name)
    db.save_chatroom(session, chat)

    if db.fetch_chat_by_name(session, chatroom_name):
        return response_factory.generate_chat_response(True, chat)
    return response_factory.generate_chat_response(False, chat)


@app.post("/connect-to-chat")
async def connect_to_chat(
        chat: schemas.ChatRoomModel, session: scoped_session = Depends(db.get_db)
):
    """Connects user to chatroom"""
    user = chat.users[0]
    messages = db.fetch_chatroom_messages(session, chat.name)
    chat.messages = messages
    if not (user_db := db.fetch_user_by_name(session, user.name)):
        return response_factory.generate_user_undefined_error_response(user)
    if not db.fetch_chat_by_name(session, chat.name):
        return response_factory.generate_chat_response(status=False, chatroom=chat)
    db.add_user_to_chatroom(session, chatroom_model=chat, user_model=user)

    if user_db in db.fetch_chat_by_name(session, chat.name).users:
        return response_factory.generate_chat_response(status=True, chatroom=chat)
    return response_factory.generate_chat_response(status=False, chatroom=chat)


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
