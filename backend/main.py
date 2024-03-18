import uvicorn
from fastapi import FastAPI, APIRouter, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.api_settings import get_api_settings
from fastapi.responses import JSONResponse

from auth.api import auth_router
from chatroom.api import chat_router
from config import settings
from sockets.api import socket_router


def get_app() -> FastAPI:
    get_api_settings.cache_clear()
    api_stg = get_api_settings()
    return FastAPI(**api_stg.fastapi_kwargs)


app = get_app()

if settings.DEV:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Add routers
router = APIRouter(prefix="/api")
router.include_router(auth_router, tags=['Auth'])
router.include_router(chat_router, tags=['Chat'])
router.include_router(socket_router, tags=['Socket'])
app.include_router(router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        headers=exc.headers,
        content={"message": exc.detail})


if __name__ == "__main__":
    uvicorn.run(app, log_level=settings.LOG_LEVEL)
