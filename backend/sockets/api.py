from datetime import datetime

from sqlalchemy.orm import scoped_session
from fastapi import WebSocket, Depends, WebSocketDisconnect
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from db.dbapi import DatabaseService
from db.schemas import MessageModel
from sockets.connection_manager import ConnectionManager

socket_router = InferringRouter()
manager = ConnectionManager()
db = DatabaseService()


@cbv(socket_router)
class WebSocketCBV:
    session: scoped_session = Depends(db.get_db)

    @socket_router.websocket('/{chatroom}/{username}')
    async def websocket_endpoint(
            self,
            websocket: WebSocket,
            username: str,
            chatroom: str):
        await manager.connect(chatroom, username, websocket)

        try:
            while True:
                text = await websocket.receive_text()
                message = MessageModel(text=text, user=username, created_at=datetime.now().strftime("%H:%M"))
                db.save_message(self.session, chatroom, message)

                await manager.send_message(chatroom, message.json())
                print(f'{username} sent "{text}" to {chatroom}')  # TODO: need to log, not print

        except WebSocketDisconnect:
            manager.disconnect(chatroom, username)
