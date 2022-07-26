from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text

from ..session import Base


class ChatRoom(Base):
    """Message Table Definition"""

    __tablename__ = "chatrooms"
    id = Column(Integer, primary_key=True)
    chat_room_id = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(Text)
    created_at = Column(Date)
    updated_at = Column(Date)

    def __repr__(self):
        return "<Messages(chat_room_id='{}', message='{}')>".format(
            self.chat_room_id, self.message
        )
