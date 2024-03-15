from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import scoped_session
from fastapi_utils.cbv import cbv

from .utils import RandomIdGenerator, create_and_get_chatroom
from chatroom.schemas import ChatRequest
from db.dbapi import DatabaseService

db = DatabaseService()
chat_router = APIRouter()


@cbv(chat_router)
class ChatCBV:
    session: scoped_session = Depends(db.get_db)

    @chat_router.post('/create-chat')
    async def create_chat(self, username):
        """Create chatroom and save to db"""
        if not db.fetch_user_by_name(self.session, username):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User does not exist",
                headers={"WWW-Authenticate": "Bearer"},
            )

        generate_id = RandomIdGenerator()
        chatroom_name = generate_id(chatroom_name=True)
        chat = create_and_get_chatroom(username, name=chatroom_name)
        db.save_chatroom(self.session, chat)

        return {"status": 201, "chatroom": chat}

    @chat_router.post('/connect-to-chat')
    async def connect_to_chat(self, req: ChatRequest):
        user = db.fetch_user_by_name(self.session, req.username)
        if not (chat := db.fetch_chat_by_name(self.session, req.chatname)):
            return {"status": 400, "chatname": req.chatname}
        if not user:
            return {"status": 400, "chatname": req.chatname}
        db.add_user_to_chatroom(self.session, chatroom_model=chat, user_model=user)
        return {"status": 200, "chatname": chat}

    @chat_router.get('/get-messages')
    def get_messages(self, chatname):
        return db.fetch_chatroom_messages(self.session, chatname)
