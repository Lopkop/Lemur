from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func

from ..session import Base


class Message(Base):
    """Message Table Definition"""

    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    chat_room_id = Column(String)
    user_id = Column(String, ForeignKey("users.user_id"))
    body = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), server_onupdate=func.now())

    def __repr__(self):
        return "<ChatRoom(chat_room_id='{}', message='{}')>".format(
            self.chat_room_id, self.body
        )
