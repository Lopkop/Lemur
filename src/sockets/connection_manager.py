from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[dict] = {}

    async def connect(self, chatroom, user_id, websocket: WebSocket):
        await websocket.accept()
        try:
            self.active_connections[chatroom][user_id] = websocket
        except KeyError:
            self.active_connections[chatroom] = {user_id: websocket}

    def disconnect(self, chatroom, user_id):
        del self.active_connections[chatroom][user_id]

    async def send_message(self, chatroom, message):
        print(self.active_connections)
        for websocket in self.active_connections[chatroom].values():
            await websocket.send_text(message)
