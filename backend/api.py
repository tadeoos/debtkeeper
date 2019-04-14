import logging
from datetime import timedelta
from typing import List

from decouple import config
from fastapi import (
    Depends,
    FastAPI,
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
from pony.orm import db_session, TransactionIntegrityError
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response, PlainTextResponse
from starlette.status import HTTP_403_FORBIDDEN

from auth import (
    ALGORITHM,
    Token,
    TokenPayload,
    authenticate_user,
    create_access_token,
    register_new_user,
)
from models import define_database
from schemas import DebtItemIn, DebtItemOut, DebtItemPatch

logger = logging.getLogger('debt_keeper')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)

app = FastAPI(
    title="DebtKeeper",
    version='v1'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['GET', 'POST', 'PATCH'],
    allow_headers=['*']
)


DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('AUTH_SECRET')

db = define_database(provider='sqlite', filename=config('DB_FILE'), create_db=True)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


@app.exception_handler(HTTPException)
async def http_exception(request, exc):
    logger.exception('')
    if exc.status_code in {204, 304}:
        return Response(b"", status_code=exc.status_code)
    return PlainTextResponse(exc.detail, status_code=exc.status_code)

@db_session
def get_current_user(token: str = Security(oauth2_scheme)):
    try:
        db.BlacklistToken.check_blacklist(token)
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
        return db.User.get(name=token_data.username).id
    except (PyJWTError, ValueError) as e:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail=f"Could not validate credentials: {e}"
        )


@app.post("/token", response_model=Token)
async def route_login_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_access_token(data={"username": form_data.username})
    return {"id": user.id, "access_token": access_token, "token_type": "bearer"}


@app.post("/register", status_code=201)
async def register(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        register_new_user(db, form_data.username, form_data.password)
    except RuntimeError:
        raise HTTPException(status_code=422, detail="User already exists")
    return {'msg': "User created successfully"}


@app.post("/logout", status_code=204)
async def logout(token: str = Security(oauth2_scheme)):
    with db_session:
        db.BlacklistToken(token=token)


@app.get("/items", response_model=List[DebtItemOut])
@db_session
def items(resolved: bool = None, kind: str = None, current_user: int = Depends(get_current_user)):
    user = db.User.get(id=current_user)
    filter_args = {}
    if resolved is not None:
        filter_args['resolved'] = [resolved]
    if kind is not None:
        filter_args['kind'] = [kind]
    return user.get_serialized_debts(**filter_args)


@app.post("/items", status_code=201)
async def create_item(item: DebtItemIn, current_user: int = Depends(get_current_user)):
    try:
        with db_session:
            db.DebtItem(**item.dict(), user=current_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except TransactionIntegrityError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.patch("/items/{item_id}", status_code=204)
async def patch_item(item_id: int, partial_data: DebtItemPatch, current_user: int = Depends(get_current_user)):
    try:
        with db_session:
            debt_item = db.DebtItem.get(id=item_id, user=current_user)
            if debt_item is None:
                raise HTTPException(status_code=404, detail=f"DebtItem with pk={item_id} not found")
            debt_item.set(**partial_data.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except TransactionIntegrityError as e:
        raise HTTPException(status_code=400, detail=str(e))
