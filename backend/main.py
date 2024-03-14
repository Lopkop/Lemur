from fastapi import FastAPI, WebSocket, Depends, WebSocketDisconnect
from sqlalchemy.orm import scoped_session
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware  # todo: later should be replaced

from sockets.connection_manager import ConnectionManager
from db.dbapi import DatabaseService
from db.schemas import MessageModel, ChatRequest
from sockets.response_factory import ResponseFactory
from utils import RandomIdGenerator, create_and_get_chatroom
from auth.api import auth_router

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

app.include_router(auth_router)


@app.post('/create-chat')
async def create_chat(username, session: scoped_session = Depends(db.get_db)):
    """Create chatroom and save to db"""
    if not db.fetch_user_by_name(session, username):
        return response_factory.generate_user_undefined_error_response(username)

    generate_id = RandomIdGenerator()
    chatroom_name = generate_id(chatroom_name=True)
    chat = create_and_get_chatroom(username, name=chatroom_name)
    db.save_chatroom(session, chat)

    return response_factory.generate_chat_response(201, chat)


@app.get('/get-messages')
def get_messages(chatname, session: scoped_session = Depends(db.get_db)):
    return db.fetch_chatroom_messages(session, chatname)


@app.post('/connect-to-chat')
async def connect_to_chat(req: ChatRequest, session: scoped_session = Depends(db.get_db)):
    user = db.fetch_user_by_name(session, req.username)
    if not (chat := db.fetch_chat_by_name(session, req.chatname)):
        return {"status": 400, "chatname": req.chatname}
    if not user:
        return {"status": 400, "chatname": req.chatname}
    db.add_user_to_chatroom(session, chatroom_model=chat, user_model=user)
    return response_factory.generate_chat_response(status=200, chatroom=chat)


@app.websocket('/{chatroom}/{username}')
async def websocket_endpoint(
        websocket: WebSocket,
        username: str,
        chatroom: str,
        session: scoped_session = Depends(db.get_db)):
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
