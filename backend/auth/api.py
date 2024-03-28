from datetime import datetime, timedelta
from fastapi import HTTPException, status, Response, Depends, Cookie
from sqlalchemy.orm import scoped_session
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

import auth.schemas as schemas
import db.schemas as db_schemas
from db.dbapi import DatabaseService
from auth.security import authenticate_user, create_access_token, token_expired, verify_user
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
        response.set_cookie(key="access_token", value=access_token,
                            expires=int(token_expires_in), httponly=True,
                            secure=True, samesite='strict')

        return schemas.AuthResponseModel(status=201, token_expires_at=float(token_expires_in) // 60)

    @auth_router.post('/login', response_model=schemas.AuthResponseModel)
    async def login(self, user: db_schemas.UserModel, response: Response):
        try:
            user = authenticate_user(self.session, user.name, user.password)
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
        response.set_cookie(key="access_token", value=access_token.token,
                            expires=int(token_expires_in), httponly=True,
                            secure=True, samesite='strict')
        response.status_code = 200
        return schemas.AuthResponseModel(status=200, token_expires_at=float(token_expires_in) // 60)

    @auth_router.get('/get_user')
    async def get_user(self, access_token: str = Cookie(None)):
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token was not provided",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user = verify_user(self.session, access_token)
        user_expires_in = (user.lifetime - datetime.now()).total_seconds() // 60
        user_model = db_schemas.UserModel(name=user.name, password=None, lifetime=user_expires_in)
        return user_model
