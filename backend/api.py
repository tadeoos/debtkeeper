import logging
import responder

from decouple import config

from models import DebtItem
from pony.orm import db_session

from views import get_user_from_headers, logout_, login_, register_

logger = logging.getLogger('debt_keeper')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)

api = responder.API(cors=True,
                    cors_params={
                        'allow_origins': ['*'],
                        'allow_methods': ['GET', 'POST'],
                        'allow_headers': ['*']
                    })

DEBUG = config('DEBUG', default=False, cast=bool)

if DEBUG:
    from test_db import db
else:
    from models import db
    db.bind(provider='sqlite', filename='debtkeeper.sqlite', create_db=True)
    db.generate_mapping(create_tables=True)


@api.route(before_request=True)
def check_token(req, resp):
    resp.headers["X-Pizza"] = "42"
    # if req.url in [logout, api]:
    #   raise UnAuthorizedError


@api.route("/api/items")
class ItemResource:

    def on_get(self, req, resp):
        with db_session:
            suc, user = get_user_from_headers(req.headers)
            if suc:
                resp.status_code = api.status_codes.HTTP_200
                resp.media = user.get_serialized_debts()
            else:
                resp.status_code = api.status_codes.HTTP_401

    async def on_post(self, req, resp):
        data = await req.media(format='json')
        with db_session:
            DebtItem.from_json(data)

        resp.status_code = api.status_codes.HTTP_201


@api.route("/auth/register")
async def register(req, resp):
    await register_(req, resp)


@api.route("/auth/login")
async def login(req, resp):
    await login_(req, resp)


@api.route("/auth/logout")
async def logout(req, resp):
    logout_(req, resp)


if __name__ == "__main__":
    api.run(debug=DEBUG, logger=logger)
