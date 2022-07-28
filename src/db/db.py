from src.db.models.chat_room_model import ChatRoom
from src.db.models.messages_model import Message
from src.db.models.user_model import User
from src.db.session import Base, Session, engine
from src.models import ChatRoomModel, MessageModel, UserModel
from src.utils import create_and_get_user

Base.metadata.create_all(engine)


class DatabaseService:
    """User Factory Class is used to create user"""

    def save_user(self, user_obj: UserModel) -> None:
        """Saves user object to database"""
        user_db_model = User(
            name=user_obj.name,
            user_id=user_obj.user_id,
        )
        Session.add(user_db_model)
        Session.commit()

    def fetch_user_by_id(self, user_id: str) -> UserModel:
        """Fetch User by user_id"""
        user_db_obj = Session.query(User).filter_by(user_id=user_id).first()
        return create_and_get_user(
            user_id=user_db_obj.user_id,
            username=user_db_obj.name,
        )

    def save_chatroom(self, chatroom_obj: ChatRoomModel) -> None:
        chatroom_db_obj = ChatRoom(chat_room_id=chatroom_obj.chatroom_id, user_one=chatroom_obj.users[0])
        Session.add(chatroom_db_obj)
        Session.commit()

    def save_message(self, chatroom_id: str, message_obj: MessageModel) -> None:
        """Saves a message to the chatroom"""
        message_obj = Message(
            chat_room_id=chatroom_id,
            user_id=message_obj.user_id,
            body=message_obj.body,
        )
        Session.add(message_obj)
        Session.commit()

    def get_chat_room_messages(
            self, chatroom_id: str, page: int = 1, size: int = 20
    ):
        """Fetch all messages in a chat room"""
        page = page - 1
        offset = page * size
        messages = (
            Session.query(Message)
                .filter_by(chat_room_id=chatroom_id)
                .order_by(Message.created_at.desc())
                .limit(size)
                .offset(offset)
                .all()
        )
        return messages
