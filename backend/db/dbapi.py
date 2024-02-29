from sqlalchemy.orm.scoping import scoped_session
from jose import jwt

from db.database import SessionLocal
from db.models import ChatRoom, Message, User, Token
from db.schemas import ChatRoomModel, MessageModel, UserModel, TokenModel
from config import SECRET_KEY


class DatabaseService:
    """DB API service"""

    @staticmethod
    def get_db():
        session = SessionLocal()
        try:
            yield session
        finally:
            session.close()

    @staticmethod
    def save_user(session: scoped_session, user_model: UserModel) -> None:
        """Saves user object to database"""
        from security import hash_password
        user = User(name=user_model.name, hashed_password=hash_password(user_model.password),
                    expires_at=user_model.lifetime)
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

    def save_chatroom(self, session: scoped_session, chatroom_model: ChatRoomModel) -> None:
        user = self.fetch_user_by_name(session, chatroom_model.users[0])
        chatroom = ChatRoom(name=chatroom_model.name, users=[user])
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

    def add_user_to_chatroom(
            self,
            session: scoped_session,
            user_model: UserModel,
            chatroom_model: ChatRoomModel,
    ):
        user = self.fetch_user_by_name(session, user_model.name)
        chat = self.fetch_chat_by_name(session, chatroom_model.name)
        user.chatroom = chat.name
        chat.users.append(user)
        session.commit()

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
        messages = session.query(Message).filter_by(chatroom=chatroom_name).all()
        # convert all message models to schemas so it could be used in application
        messages = [dict(user=message.user, text=message.text) for message in messages]
        return messages

    @staticmethod
    def fetch_token_by_username(session: scoped_session, name: str):
        token = session.query(Token).filter_by(user=name).first()
        return token

    def fetch_user_by_access_token(self, session, access_token):
        decoded = jwt.decode(access_token, SECRET_KEY)
        return self.fetch_user_by_name(session, decoded['name'])
