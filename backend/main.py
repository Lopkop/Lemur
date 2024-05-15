import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.api_settings import get_api_settings

from config import settings
from api import router, exc_handlers
from api.middleware import log_request_middleware


def get_app() -> FastAPI:
    get_api_settings.cache_clear()
    api_stg = get_api_settings()
    return FastAPI(**api_stg.fastapi_kwargs)


app = get_app()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(log_request_middleware)

for handler in exc_handlers:
    app.add_exception_handler(handler[0], handler[1])

# Add routers
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, log_level=settings.LOG_LEVEL)
