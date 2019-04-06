from responder import status_codes
from pony.orm import db_session

from fbcrypt import check_password_hash
from models import User, BlacklistToken


def register_new_user(username, password):
    with db_session:
        if User.get(name=username):
            return False, {}
        user = User(name=username, password=password)
        user.flush()
        return True, {'token': user.encode_auth_token()}


def get_token(headers):
    auth_header = headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ""
    return auth_token


def get_user_from_headers(headers):
    response = 'Provide a valid auth token'
    auth_token = get_token(headers)
    if auth_token:
        with db_session:
            response = User.decode_auth_token(auth_token)
            if isinstance(response, int):
                with db_session:
                    user = User.get(id=response)
                    if user:
                        return True, user
                    else:
                        return False, "User not found"
    return False, response


def logout_(req, resp):
    if req.method == 'post':
        auth_token = get_token(req.headers)
        if auth_token:
            response = User.decode_auth_token(auth_token)
            if not isinstance(response, str):
                with db_session:
                    BlacklistToken(token=auth_token)
                resp.status_code = status_codes.HTTP_200
                resp.media = {
                    'status': 'success',
                    'message': 'Successfully logged out',
                }
            else:
                resp.status_code = status_codes.HTTP_401
                resp.media = {
                    'status': 'fail',
                    'message': response
                }
        else:
            resp.status_code = status_codes.HTTP_403
            resp.media = {
                'status': 'fail',
                'message': 'Provide a valid auth token'
            }
    else:
        resp.status_code = status_codes.HTTP_400
        resp.media = {'error': 'method not supported'}


async def login_(req, resp):
    if req.method == 'post':
        data = await req.media(format='json')
        username = data.get('username')
        password = data.get('password')
        with db_session:
            user = User.get(name=username)
        if user:
            if check_password_hash(user.password, password):
                token = user.encode_auth_token()
                resp.status_code = status_codes.HTTP_200
                resp.media = {
                    'id': user.id,
                    'message': 'Successfully logged in',
                    'token': token.decode()
                }
            else:
                resp.status_code = status_codes.HTTP_422
                resp.media = {
                    'status': 'fail',
                    'message': 'Wrong password'
                }
        else:
            resp.status_code = status_codes.HTTP_404
            resp.media = {'error': 'User does not exist'}
    else:
        resp.status_code = status_codes.HTTP_400
        resp.media = {'error': 'method not supported'}


async def register_(req, resp):
    if req.method == 'post':
        data = await req.media(format='json')
        username = data.get('username')
        password = data.get('password')
        if username and password:
            success = register_new_user(username, password)
            if success[0]:
                resp.status_code = status_codes.HTTP_201
                resp.media = {'msg': f'User {username} created'}.update(success[1])
            else:
                resp.status_code = status_codes.HTTP_422
                resp.media = {'msg': f'User {username} already exists'}
        else:
            resp.status_code = status_codes.HTTP_400
            resp.media = {'error': 'expecting username and password'}
    else:
        resp.status_code = status_codes.HTTP_400
        resp.media = {'error': 'method not supported'}
