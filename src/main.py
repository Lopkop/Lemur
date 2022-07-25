import asyncio
from fastapi import FastAPI
from fastapi import WebSocket

app = FastAPI()

@app.websocket("/sign_up")
async def sign_up(websocket: WebSocket):
    """ Signs Up New Users """
    connection = ConnectionHandler(websocket)
    request = connection.get_request()
    # Create User Object
    # Save User To DB
    response = {}
    connection.send_response(response)
