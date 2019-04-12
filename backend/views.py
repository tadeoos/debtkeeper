from pony.orm import db_session

from models import (
    BlacklistToken,
    User,
)
from responder import status_codes


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
            with db_session:
                response = User.decode_auth_token(auth_token)
                if not isinstance(response, str):
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
