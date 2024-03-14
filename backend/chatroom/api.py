from fastapi import APIRouter, Depends
from sqlalchemy.orm import scoped_session

from sockets.response_factory import ResponseFactory
from .utils import RandomIdGenerator, create_and_get_chatroom
from db.schemas import ChatRequest
from db.dbapi import DatabaseService

db = DatabaseService()
chat_router = APIRouter()
response_factory = ResponseFactory()


@chat_router.post('/create-chat')
async def create_chat(username, session: scoped_session = Depends(db.get_db)):
    """Create chatroom and save to db"""
    if not db.fetch_user_by_name(session, username):
        return response_factory.generate_user_undefined_error_response(username)

    generate_id = RandomIdGenerator()
    chatroom_name = generate_id(chatroom_name=True)
    chat = create_and_get_chatroom(username, name=chatroom_name)
    db.save_chatroom(session, chat)

    return response_factory.generate_chat_response(201, chat)


@chat_router.post('/connect-to-chat')
async def connect_to_chat(req: ChatRequest, session: scoped_session = Depends(db.get_db)):
    user = db.fetch_user_by_name(session, req.username)
    if not (chat := db.fetch_chat_by_name(session, req.chatname)):
        return {"status": 400, "chatname": req.chatname}
    if not user:
        return {"status": 400, "chatname": req.chatname}
    db.add_user_to_chatroom(session, chatroom_model=chat, user_model=user)
    return response_factory.generate_chat_response(status=200, chatroom=chat)


@chat_router.get('/get-messages')
def get_messages(chatname, session: scoped_session = Depends(db.get_db)):
    return db.fetch_chatroom_messages(session, chatname)
