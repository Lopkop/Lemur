from passlib.context import CryptContext
from jose import JWTError, jwt
from config import SECRET_KEY

from db.dbapi import DatabaseService

db = DatabaseService()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"


def authenticate_user(session, name: str, password: str):
    user = db.fetch_user_by_name(session, name)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password):
    return pwd_context.hash(password)


def create_access_token(data: dict):
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    decoded = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)
    print(decoded)
    return decoded
