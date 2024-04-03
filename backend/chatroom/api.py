from fastapi import Depends, HTTPException, status, Cookie
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.orm import scoped_session
from fastapi_utils.cbv import cbv

from .utils import RandomIdGenerator, create_and_get_chatroom
from chatroom.schemas import ChatRequest
from db.dbapi import DatabaseService
from auth import security
from config import logger

db = DatabaseService()
chat_router = InferringRouter()


@cbv(chat_router)
class ChatCBV:
    session: scoped_session = Depends(db.get_db)

    @chat_router.post('/create-chat')
    async def create_chat(self, username, access_token: str = Cookie(None)):
        """Create chatroom and save to db"""
        if not (access_token and security.verify_user(self.session, access_token)):
            logger.info(username, access_token)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
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
        db.add_user_to_chatroom(self.session, username, chat.name)

        return {"status": 201, "chatroom": chat}

    @chat_router.post('/connect-to-chat')
    async def connect_to_chat(self, req: ChatRequest, access_token: str = Cookie(None)):
        if not access_token or not (user := security.verify_user(self.session, access_token)):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not (chat := db.fetch_chat_by_name(self.session, req.chatname)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="There is no chat with that name",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if user.name in {usr.user for usr in chat.users}:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already in chat",
                headers={"WWW-Authenticate": "Bearer"},
            )
        db.add_user_to_chatroom(self.session, chatroom_name=chat.name, username=user.name)
        return {"status": 200, "chatname": chat.name}

    @chat_router.get('/get-messages/{chatroom_name}')
    def get_messages(self, chatroom_name, access_token: str = Cookie(None)):
        if not (access_token and security.verify_user(self.session, access_token)):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return db.fetch_chatroom_messages(self.session, chatroom_name)
