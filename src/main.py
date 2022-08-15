from typing import Union

from fastapi import FastAPI, WebSocket, Depends
from sqlalchemy.orm import scoped_session

from sockets.connection_handler import ConnectionHandler
from src.db.dbapi import DatabaseService
from src.db import schemas
from src.sockets.response_factory import ResponseFactory
from src.utils import RandomIdGenerator, create_and_get_chatroom

app = FastAPI()
db = DatabaseService()
response = ResponseFactory()


@app.post("/sign-up", response_model=schemas.SignUpResponseModel)
async def sign_up(user: schemas.UserModel, session: scoped_session = Depends(db.get_db)):
    """Signs Up New Users"""
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


# TODO: finish other api's
@app.websocket("/send_message")
async def send_message(websocket: WebSocket):
    """Sends Message to Given Chatroom"""
    connection = ConnectionHandler(websocket)
    request = connection.get_request()
    message = {}  # Create Message Object
    # Save Message Object to DB
    response = {}  # uses ResponseFactory to generate Response JSON from Message Object
    connection.send_response(response)


@app.websocket("/get_messages")
async def get_message(websocket: WebSocket):
    """Gets All Messages Of Given Chatroom"""
    connection = ConnectionHandler(websocket)
    request = connection.get_request()
    chatroom = (
        {}
    )  # Get messsage object from chatroom - something like database_client.get_chatroom_data(chatroom_id)
    response = {}  # uses ResponseFactory to generate Response JSON from Chatroom Object
    connection.send_response(response)
