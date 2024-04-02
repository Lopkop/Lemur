from functools import lru_cache
from typing import Iterator

from fastapi_utils.session import FastAPISessionMaker
from sqlalchemy import asc
from sqlalchemy.orm import Session
from sqlalchemy.orm.scoping import scoped_session
from jose import jwt

from db.models import ChatRoom, Message, User, Token, UserChatRoom
from db.schemas import ChatRoomModel, MessageModel, UserModel, TokenModel
from config import settings


def save_chatroom(session: scoped_session, chatroom_model: ChatRoomModel, username: str) -> None:
    chatroom = ChatRoom(name=chatroom_model.name)
    session.add(chatroom)
    session.commit()
    session.refresh(chatroom)


class DatabaseService:
    """DB API service"""

    def get_db(self) -> Iterator[Session]:
        """FastAPI dependency that provides a sqlalchemy session"""
        yield from self._get_fastapi_sessionmaker().get_db()

    @staticmethod
    @lru_cache()
    def _get_fastapi_sessionmaker() -> FastAPISessionMaker:
        return FastAPISessionMaker(settings.DATABASE_URL)

    @staticmethod
    def save_user(session: scoped_session, user_model: UserModel) -> None:
        """Saves user object to database"""
        from auth.security import hash_password
        user = User(name=user_model.name, hashed_password=hash_password(user_model.password),
                    lifetime=user_model.lifetime)
        session.add(user)
        session.commit()
        session.refresh(user)

    @staticmethod
    def save_token(session: scoped_session, token: TokenModel, expires_at, user_name: str) -> None:
        """Saves token object to database"""
        token = Token(token=token, expires_at=expires_at, user=user_name)
        session.add(token)
        session.commit()
        session.refresh(token)

    @staticmethod
    def save_chatroom(session: scoped_session, chatroom_model: ChatRoomModel) -> None:
        chatroom = ChatRoom(name=chatroom_model.name)
        session.add(chatroom)
        session.commit()
        session.refresh(chatroom)

    @staticmethod
    def save_message(
            session: scoped_session, chatroom_name: str, message_model: MessageModel
    ) -> None:
        """Saves a message to the chatroom"""
        message = Message(
            chatroom=chatroom_name,
            user=message_model.user,
            text=message_model.text,
        )
        session.add(message)
        session.commit()
        session.refresh(message)

    @staticmethod
    def add_user_to_chatroom(
            session: scoped_session,
            username: str,
            chatroom_name: str
    ):
        user_chatroom = UserChatRoom(chatroom_name=chatroom_name, user=username)
        session.add(user_chatroom)
        session.commit()
        session.refresh(user_chatroom)

    @staticmethod
    def fetch_user_by_name(session: scoped_session, username: str) -> User:
        """Fetch User by username"""
        user = session.query(User).filter_by(name=username).first()
        return user

    @staticmethod
    def fetch_chat_by_name(session: scoped_session, name: str) -> ChatRoom:
        chat = session.query(ChatRoom).filter_by(name=name).first()
        return chat

    @staticmethod
    def fetch_chatroom_messages(session: scoped_session, chatroom_name: str):
        """Fetch all messages in a chat room"""
        messages = session.query(Message).filter_by(chatroom=chatroom_name).order_by(asc(Message.created_at)).all()
        messages = [dict(user=message.user,
                         text=message.text,
                         created_at=message.created_at.strftime("%H:%M"))
                    for message in messages]
        return messages

    @staticmethod
    def fetch_token_by_username(session: scoped_session, name: str):
        token = session.query(Token).filter_by(user=name).first()
        return token

    def fetch_user_by_access_token(self, session, access_token):
        decoded = jwt.decode(access_token, settings.SECRET_KEY)
        return self.fetch_user_by_name(session, decoded['name'])

    @staticmethod
    def fetch_access_token_by_name(session, name):
        return session.query(Token).filter_by(token=name).first()

    def remove_user(self, session: scoped_session, username: str):
        user = self.fetch_user_by_name(session, username)
        session.delete(user)  # automatically removes token associated with the user
        session.commit()
