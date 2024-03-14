from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, status, Response, Depends
from sqlalchemy.orm import scoped_session

import auth.schemas as schemas
import db.schemas as db_schemas
from db.dbapi import DatabaseService
from auth.security import authenticate_user, create_access_token, token_expired_check
from sockets.response_factory import ResponseFactory
from auth.exceptions import LoginFailed, UserExpired

response_factory = ResponseFactory()
db = DatabaseService()
auth_router = APIRouter()


@auth_router.post('/sign-up', response_model=schemas.AuthResponseModel)
async def sign_up(user: db_schemas.UserModel, response: Response, session: scoped_session = Depends(db.get_db)):
    if db.fetch_user_by_name(session, user.name):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User with this name already exists',
            headers={"WWW-Authenticate": "Bearer"},
        )

    current_time = datetime.now()
    expires_delta = timedelta(hours=user.lifetime)
    expiration_time = current_time + expires_delta
    user.lifetime = expiration_time

    db.save_user(session, user)
    access_token = create_access_token({"name": user.name})
    db.save_token(session, access_token, expiration_time, user.name)

    token_expires_in = (expiration_time - datetime.now()).total_seconds()
    response.set_cookie(key="access_token", value=access_token, httponly=True, expires=int(token_expires_in),
                        samesite='strict', secure=True)

    return schemas.AuthResponseModel(status=201, access_token=access_token,
                                     token_expires_at=float(token_expires_in) // 60)


@auth_router.post('/login', response_model=schemas.AuthResponseModel)
async def login(user: db_schemas.UserModel, response: Response, session: scoped_session = Depends(db.get_db)):
    try:
        user = authenticate_user(session, user.name, user.password)
        token_expired_check(session, user.name)
    except LoginFailed:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except UserExpired:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your account was deleted",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = db.fetch_token_by_username(session, user.name)
    token_expires_in = (access_token.expires_at - datetime.now()).total_seconds()
    response.set_cookie(key="access_token", value=access_token.token, httponly=True,
                        expires=int(token_expires_in), samesite='strict', secure=True)
    response.status_code = 200
    return schemas.AuthResponseModel(status=200, access_token=access_token.token,
                                     token_expires_at=float(token_expires_in) // 60)


@auth_router.get('/get_user/{token}')
async def get_user(token: str, session: scoped_session = Depends(db.get_db)):
    user = db.fetch_user_by_access_token(session, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        token_expired_check(session, user.name)
    except LoginFailed:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except UserExpired:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your account was deleted",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user.hashed_password = None
    return user
