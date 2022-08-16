import json


class ConnectionHandler:
    def __init__(self, socket):
        self.socket = socket

    async def get_request(self) -> dict:
        """Returns json request from client"""
        return await self.process_incoming_connection()

    async def send_response(self, response: dict) -> None:
        """Sends json response to the client"""
        await self.socket.send_text(json.dumps(response))

    async def process_incoming_connection(self) -> dict:
        """Accepts connection and returns request"""
        await self.socket.accept()
        request = await self.socket.receive_text()
        return request
