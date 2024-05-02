from fastapi import APIRouter, HTTPException
from fastapi.exceptions import RequestValidationError

from api.auth.api import auth_router
from api.chatroom.api import chat_router
from api.sockets.api import socket_router

from api.exception_handlers import (http_exception_handler,
                                    unhandled_exception_handler,
                                    request_validation_exception_handler
                                    )

router = APIRouter(prefix='/api')

for r in (auth_router, chat_router, socket_router):
    router.include_router(r)

exc_handlers = {(HTTPException, http_exception_handler),
                (Exception, unhandled_exception_handler),
                (RequestValidationError, request_validation_exception_handler),
                }
