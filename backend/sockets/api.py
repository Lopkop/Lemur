from sqlalchemy.orm import scoped_session
from fastapi import APIRouter, WebSocket, Depends, WebSocketDisconnect

from db.dbapi import DatabaseService
from db.schemas import MessageModel
from sockets.connection_manager import ConnectionManager

socket_router = APIRouter()
manager = ConnectionManager()
db = DatabaseService()


@socket_router.websocket('/{chatroom}/{username}')
async def websocket_endpoint(
        websocket: WebSocket,
        username: str,
        chatroom: str,
        session: scoped_session = Depends(db.get_db)):
    await manager.connect(chatroom, username, websocket)

    try:
        while True:
            text = await websocket.receive_text()
            message = MessageModel(text=text, user=username)
            db.save_message(session, chatroom, message)

            await manager.send_message(chatroom, message.json())
            print(f'{username} sent "{text}" to {chatroom}')  # need to log, not print

    except WebSocketDisconnect:
        manager.disconnect(chatroom, username)
