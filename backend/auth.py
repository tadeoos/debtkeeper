from datetime import (
    datetime,
    timedelta,
)

import jwt
from decouple import config
from passlib.context import CryptContext
from pony.orm import db_session
from pydantic import BaseModel


SECRET_KEY = config('AUTH_SECRET')

ALGORITHM = "HS256"
TOKEN_SUBJECT = "access"
ACCESS_TOKEN_EXPIRE_MINUTES = config("TOKEN_EXPIRES_MINUTES", default=15, cast=int)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Token(BaseModel):
    id: int
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    username: str = None


def register_new_user(db, username, password):
    with db_session:
        if db.User.get(name=username):
            raise RuntimeError("User already exists")
        user = db.User(name=username, password=password)
        user.flush()
        return True


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db, username: str, password: str):
    with db_session:
        user = db.User.get(name=username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(*, data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "sub": TOKEN_SUBJECT})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
