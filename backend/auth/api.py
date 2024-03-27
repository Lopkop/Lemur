from datetime import datetime, timedelta
from fastapi import HTTPException, status, Response, Depends
from sqlalchemy.orm import scoped_session
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

import auth.schemas as schemas
import db.schemas as db_schemas
from db.dbapi import DatabaseService
from auth.security import authenticate_user, create_access_token, token_expired_check
from auth.exceptions import LoginFailed, UserExpired

db = DatabaseService()
auth_router = InferringRouter()


@cbv(auth_router)
class Auth:
    session: scoped_session = Depends(db.get_db)

    @auth_router.post('/sign-up', response_model=schemas.AuthResponseModel)
    async def sign_up(self, user: db_schemas.UserModel, response: Response):
        if db.fetch_user_by_name(self.session, user.name):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='User with this name already exists',
                headers={"WWW-Authenticate": "Bearer"},
            )

        current_time = datetime.now()
        expires_delta = timedelta(hours=user.lifetime)
        expiration_time = current_time + expires_delta
        user.lifetime = expiration_time

        db.save_user(self.session, user)
        access_token = create_access_token({"name": user.name})
        db.save_token(self.session, access_token, expiration_time, user.name)

        token_expires_in = (expiration_time - datetime.now()).total_seconds()
        response.set_cookie(key="access_token", value=access_token, httponly=True, expires=int(token_expires_in),
                            samesite='strict', secure=True)

        return schemas.AuthResponseModel(status=201, access_token=access_token,
                                         token_expires_at=float(token_expires_in) // 60)

    @auth_router.post('/login', response_model=schemas.AuthResponseModel)
    async def login(self, user: db_schemas.UserModel, response: Response):
        try:
            user = authenticate_user(self.session, user.name, user.password)
            token_expired_check(self.session, user.name)
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
        access_token = db.fetch_token_by_username(self.session, user.name)
        token_expires_in = (access_token.expires_at - datetime.now()).total_seconds()
        response.set_cookie(key="access_token", value=access_token.token, httponly=True,
                            expires=int(token_expires_in), samesite='strict', secure=True)
        response.status_code = 200
        return schemas.AuthResponseModel(status=200, access_token=access_token.token,
                                         token_expires_at=float(token_expires_in) // 60)

    @auth_router.get('/get_user/{token}')
    async def get_user(self, token: str):
        user = db.fetch_user_by_access_token(self.session, token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user_expires_in = (user.lifetime - datetime.now()).total_seconds()//60
        user_model = db_schemas.UserModel(name=user.name, password=None, lifetime=user_expires_in)
        try:
            token_expired_check(self.session, user.name)
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
        return user_model
