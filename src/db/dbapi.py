from sqlalchemy.orm import Session

from src.db.models import ChatRoom, Message, User
from src.db.schemas import ChatRoomModel, MessageModel, UserModel


class DatabaseService:
    """DB API service"""

    @staticmethod
    def save_user(db: Session, user_model: UserModel) -> None:
        """Saves user object to database"""
        user = User(name=user_model.name)
        db.add(user)
        db.commit()
        db.refresh(user)

    def save_chatroom(self, db: Session, chatroom_model: ChatRoomModel) -> None:
        user = self.fetch_user_by_name(db, chatroom_model.users[0].name)
        chatroom = ChatRoom(name=chatroom_model.name, users=[user])
        db.add(chatroom)
        db.commit()
        db.refresh(chatroom)

    @staticmethod
    def save_message(db: Session, chatroom_name: str, message_model: MessageModel) -> None:
        """Saves a message to the chatroom"""
        message = Message(
            chatroom=chatroom_name,
            user=message_model.user,
            text=message_model.text,
        )
        db.add(message)
        db.commit()
        db.refresh(message)

    def add_user_to_chatroom(
            self, db: Session, user_model: UserModel, chatroom_model: ChatRoomModel
    ):
        user = self.fetch_user_by_name(db, user_model.name)
        chat = self.fetch_chat_by_name(db, chatroom_model.name)
        user.chatroom = chat.name
        chat.users.append(user)
        db.commit()

    @staticmethod
    def fetch_user_by_name(db: Session, username: str) -> User:
        """Fetch User by username"""
        user = db.query(User).filter_by(name=username).first()
        return user

    @staticmethod
    def fetch_chat_by_name(db: Session, name: str) -> ChatRoom:
        chat = db.query(ChatRoom).filter_by(name=name).first()
        return chat

    @staticmethod
    def fetch_chatroom_messages(db: Session, chatroom_name: str, page: int = 1, size: int = 20):
        """Fetch all messages in a chat room"""
        page = page - 1
        offset = page * size
        messages = (
            db.query(Message)
                .filter_by(chatroom=chatroom_name)
                .order_by(Message.created_at.desc())
                .limit(size)
                .offset(offset)
                .all()
        )
        return messages
