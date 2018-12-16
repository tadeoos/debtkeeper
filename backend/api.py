import logging
import responder

from decouple import config

from fbcrypt import check_password_hash
from models import User, BlacklistToken
from pony.orm import db_session

logger = logging.getLogger(__name__)

api = responder.API()

DEBUG = config('DEBUG', default=False, cast=bool)

if DEBUG:
    from test_db import db
else:
    from models import db
    db.bind(provider='sqlite', filename='debtkeeper.sqlite', create_db=True)
    db.generate_mapping(create_tables=True)


def register_new_user(username, password):
    with db_session:
        if User.get(name=username):
            return False, {}
        user = User(name=username, password=password)
        user.flush()
        return True, {'auth_token': user.encode_auth_token()}


@api.route("/auth/register")
async def register(req, resp):
    if req.method == 'post':
        data = await req.media(format='json')
        username = data.get('username')
        password = data.get('password')
        if username and password:
            success = register_new_user(username, password)
            if success[0]:
                resp.status_code = api.status_codes.HTTP_201
                resp.media = {'msg': f'User {username} created'}.update(success[1])
            else:
                resp.status_code = api.status_codes.HTTP_422
                resp.media = {'msg': f'User {username} already exists'}
        else:
            resp.status_code = api.status_codes.HTTP_400
            resp.media = {'error': 'expecting username and password'}
    else:
        resp.status_code = api.status_codes.HTTP_400
        resp.media = {'error': 'method not supported'}


@api.route("/auth/login")
async def login(req, resp):
    if req.method == 'post':
        data = await req.media(format='json')
        username = data.get('username')
        password = data.get('password')
        user = User.get(name=username)
        if user:
            if check_password_hash(user.password, password):
                token = user.encode_auth_token()
                resp.status_code = api.status_codes.HTTP_200
                resp.media = {
                    'status': 'success',
                    'message': 'Successfully logged in',
                    'auth_token': token.decode()
                }
            else:
                resp.status_code = api.status_codes.HTTP_422
                resp.media = {
                    'status': 'fail',
                    'message': 'Wrong password'
                }
        else:
            resp.status_code = api.status_codes.HTTP_404
            resp.media = {'error': 'User does not exist'}
    else:
        resp.status_code = api.status_codes.HTTP_400
        resp.media = {'error': 'method not supported'}


@api.route("/auth/logout")
async def logout(req, resp):
    if req.method == 'post':
        auth_header = req.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            response = User.decode_auth_token(auth_token)
            if not isinstance(response, str):
                with db_session:
                    BlacklistToken(token=auth_token)
                resp.status_code = api.status_codes.HTTP_200
                resp.media = {
                    'status': 'success',
                    'message': 'Successfully logged out',
                }
            else:
                resp.status_code = api.status_codes.HTTP_401
                resp.media = {
                    'status': 'fail',
                    'message': response
                }
        else:
            resp.status_code = api.status_codes.HTTP_403
            resp.media = {
                'status': 'fail',
                'message': 'Provide a valid auth token'
            }
    else:
        resp.status_code = api.status_codes.HTTP_400
        resp.media = {'error': 'method not supported'}


if __name__ == "__main__":
    api.run(debug=DEBUG)
