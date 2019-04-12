import datetime

import jwt
from decouple import config
from passlib.context import CryptContext
from pony import orm

from schemas import DebtItemSchema


def define_entities(db):

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    class User(db.Entity):

        _table_ = 'users'

        name = orm.Required(str, unique=True)
        email = orm.Optional(str)
        password = orm.Required(str)
        debts = orm.Set("DebtItem")
        created = orm.Optional(datetime.datetime)

        VALID_TOKEN_TIME = 3600

        def before_insert(self):

            self.password = pwd_context.hash(self.password)
            self.created = datetime.datetime.now()

        @staticmethod
        def decode_auth_token(auth_token):
            """
            Decodes the auth token
            :param auth_token:
            :return: integer|string
            """
            try:
                payload = jwt.decode(auth_token, config('SECRET_KEY'), algorithms=['HS256'])
                is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
                if is_blacklisted_token:
                    return 'Token blacklisted. Please log in again.'
                else:
                    return payload['sub']
            except jwt.ExpiredSignatureError:
                return 'Signature expired. Please log in again.'
            except jwt.InvalidTokenError:
                return 'Invalid token. Please log in again.'

        def get_serialized_debts(self):
            return [di.serialize() for di in self.debts]

    class BlacklistToken(db.Entity):
        """
        Token Model for storing JWT tokens
        """
        _table_ = 'blacklist_tokens'

        token = orm.Required(str, unique=True)
        blacklisted_on = orm.Optional(datetime.datetime)

        def before_insert(self):
            self.blacklisted_on = datetime.datetime.now()

        @staticmethod
        def check_blacklist(auth_token):
            # check whether auth token has been blacklisted
            if BlacklistToken.get(token=str(auth_token)):
                return True
            return False

    class DebtItem(db.Entity):
        _table_ = 'debts'

        kind = orm.Required(str, py_check=lambda val: val.lower() in ['loan', 'debt'])
        due_date = orm.Required(datetime.date, py_check=lambda val: val > datetime.datetime.now().date())
        created = orm.Optional(datetime.datetime)
        who = orm.Required(str)
        what = orm.Required(str)
        resolved = orm.Required(bool, default=False)
        user = orm.Required(User)

        orm.composite_key(who, what, due_date, kind)

        def before_insert(self):
            self.created = datetime.datetime.now()

        def serialize(self):
            schema = DebtItemSchema(**self.to_dict())
            return schema


def define_database(**db_params):
    db = orm.Database(**db_params)
    define_entities(db)
    db.generate_mapping(create_tables=True)
    return db
