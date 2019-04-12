import logging
from datetime import timedelta

import fastapi
from decouple import config
from fastapi import (
    Depends,
    HTTPException,
    Security,
)
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)
from jwt import (
    PyJWTError,
    decode,
)
from pony.orm import db_session
from starlette.middleware.cors import CORSMiddleware
from starlette.status import HTTP_403_FORBIDDEN

from auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    Token,
    TokenPayload,
    authenticate_user,
    create_access_token,
    register_new_user,
)
from models import define_database


logger = logging.getLogger('debt_keeper')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)

app = fastapi.FastAPI(
    title="DebtKeeper",
    version='v1'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['GET', 'POST'],
    allow_headers=['*']
)


DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('AUTH_SECRET')

db = define_database(provider='sqlite', filename=config('DB_FILE'), create_db=True)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def get_current_user(token: str = Security(oauth2_scheme)):
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    with db_session:
        return db.User.get(name=token_data.username).name


# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


@app.post("/token", response_model=Token)
async def route_login_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": form_data.username}, expires_delta=access_token_expires
    )
    return {"id": user.id, "access_token": access_token, "token_type": "bearer"}


@app.post("/register")
async def register(form_data: OAuth2PasswordRequestForm = Depends(), status_code=201):
    try:
        register_new_user(db, form_data.username, form_data.password)
    except RuntimeError:
        raise HTTPException(status_code=422, detail="User already exists")
    return {'msg': "User created successfully"}


# @app.post("/auth/logout")
# async def logout(current_user: User = Depends(get_current_user), token: str = Security(oauth2_scheme)):
#     logout_(req, resp)

@app.get("/api/items")
@db_session
def items(current_user = Depends(get_current_user)):
    # import ipdb; ipdb.set_trace()
    user = db.User.get(name=current_user)
    return user.get_serialized_debts()
# @api.route("/api/items")
# class ItemResource:
#
#     def on_get(self, req, resp):
#         with db_session:
#             suc, user = get_user_from_headers(req.headers)
#             if suc:
#                 resp.status_code = api.status_codes.HTTP_200
#                 resp.media = user.get_serialized_debts()
#             else:
#                 resp.status_code = api.status_codes.HTTP_401
#
#     async def on_post(self, req, resp):
#         data = await req.media(format='json')
#         with db_session:
#             DebtItem.from_json(data)
#
#         resp.status_code = api.status_codes.HTTP_201
#
#     def on_patch(self, req, resp):
#         with db_session:
#             suc, user = get_user_from_headers(req.headers)
#             if suc:
#                 resp.status_code = api.status_codes.HTTP_200
#                 resp.media = user.get_serialized_debts()
#             else:
#                 resp.status_code = api.status_codes.HTTP_401
