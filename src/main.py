import asyncio

from fastapi import FastAPI, WebSocket

from sockets.connection_handler import ConnectionHandler

app = FastAPI()


# Instantiate DatabaseClient


@app.websocket("/sign_up")
async def sign_up(websocket: WebSocket):
    """Signs Up New Users"""
    connection = ConnectionHandler(websocket)
    request = connection.get_request()
    # Create User Object
    # Save User To DB
    response = {}  # uses ResponseFactory to generate Response JSON from User Object
    connection.send_response(response)


@app.websocket("/send_message")
async def send_message(websocket: WebSocket):
    """Sends Message to Given Chatroom"""
    connection = ConnectionHandler(websocket)
    request = connection.get_request()
    message = {}  # Create Message Object
    # Save Message Object to DB
    response = {}  # uses ResponseFactory to generate Response JSON from Message Object
    connection.send_response(response)


@app.websocket("/get_messages")
async def get_message(websocket: WebSocket):
    """Gets All Messages Of Given Chatroom"""
    connection = ConnectionHandler(websocket)
    request = connection.get_request()
    chatroom = (
        {}
    )  # Get messsage object from chatroom - something like database_client.get_chatroom_data(chatroom_id)
    response = {}  # uses ResponseFactory to generate Response JSON from Chatroom Object
    connection.send_response(response)
