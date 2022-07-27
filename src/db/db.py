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
            chat_room_id=user_obj.chatroom_id,
            user_id=user_obj.user_id,
        )
        Session.add(user_db_model)
        Session.commit()

    def fetch_user_by_id(self, user_id: str) -> UserModel:
        """Get User by id

        Fetch user object by querying on name
        :param name:
        :return:
        """
        user_db_obj = Session.query(User).filter_by(user_id=id).first()
        return create_and_get_user(
            user_id=user_db_obj.user_id,
            chatroom_id=user_db_obj.chat_room_id,
            username=user_db_obj.name,
        )

    def save_messaage(self, chatroom_obj: ChatRoomModel, message_obj: MessageModel):
        """
        Saves a message to chatroom

        :param chatroom_obj:
        :param message_obj:
        :return:
        """
        user_item = Session.query(User).filter_by(user_id=message_obj.user_id).first()
        message_obj = Message(
            chat_room_id=chatroom_obj.chatroom_id,
            user_id=user_item.id,
            body=message_obj.body,
        )
        Session.add(message_obj)
        Session.commit()

    def get_chat_room_messages(
        self, chatroom_obj: ChatRoomModel, page: int = 1, size: int = 20
    ):
        """
            Fetch all messages in a chat room

        :param chatroom_id:
        :param page:
        :param size:
        :return:
        """
        page = page - 1
        offset = page * size
        chatroom_obj.messages = (
            Session.query(Message)
            .filter_by(chat_room_id=chatroom_obj.chatroom_id)
            .order_by(Message.created_at.desc())
            .limit(size)
            .offset(offset)
            .all()
        )
        return chatroom_obj
