from src.db.models.chat_room_model import ChatRoom
from src.db.models.user_model import User
from src.db.session import Base, Session, engine

Base.metadata.create_all(engine)


class UserFactory:
    """User Factory Class is used to create user"""

    def save_user(self, user_obj):
        """Saves user object to database"""
        user_db_model = User(name=user_obj.name, chat_room_id=user_obj.chatroom_id)
        Session.add(user_db_model)
        Session.commit()
        return user_obj

    def fetch_user_by_id(self, id):
        """Get User by id

        Fetch user object by querying on name
        :param name:
        :return:
        """
        return Session.query(User).filter_by(id=id).first()


class ChatRoomFactory:
    """ChatRoom Factory to create messages"""

    def save_messaage(self, chatroom_id: str, user_id: int, message: str):
        """
        Saves a message to chatroom

        :param chat_room_obj:
        :return:
        """
        chat_room_obj = ChatRoom(
            chat_room_id=chatroom_id, user_id=user_id, message=message
        )
        Session.add(chat_room_obj)
        Session.commit()
        return chat_room_obj

    def get_chat_room_messages(self, chatroom_id: str, page: int = 1, size: int = 20):
        """
            Fetch all messages in a chat room

        :param chatroom_id:
        :param page:
        :param size:
        :return:
        """
        page = page - 1
        offset = page * size
        return (
            Session.query(ChatRoom)
            .filter_by(chat_room_id=chatroom_id)
            .order_by(ChatRoom.created_at.desc())
            .limit(size)
            .offset(offset)
            .all()
        )
