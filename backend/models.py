import datetime
import json

from decouple import config
import jwt
from pony import orm

from fbcrypt import generate_password_hash
from schemas import DebtItemSchema

db = orm.Database()


class User(db.Entity):

    _table_ = 'users'

    name = orm.Required(str, unique=True)
    email = orm.Optional(str)
    password = orm.Required(str)
    debts = orm.Set("DebtItem")
    created = orm.Optional(datetime.datetime)

    def before_insert(self):
        hashed_password = generate_password_hash(self.password).decode()
        self.password = hashed_password
        self.created = datetime.datetime.now()

    def encode_auth_token(self, user_id=None):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, hours=0, seconds=0),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id or self.id
            }
            return jwt.encode(
                payload,
                config('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

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
        res = BlacklistToken.get(token=str(auth_token))
        if res:
            return True
        else:
            return False


class DebtItem(db.Entity):
    _table_ = 'debts'

    name = orm.Required(str)
    kind = orm.Required(str)
    due_date = orm.Required(datetime.date)
    created = orm.Optional(datetime.datetime)
    who = orm.Required(str)
    what = orm.Required(str)
    user = orm.Required(User)

    def before_insert(self):
        self.created = datetime.datetime.now()

    def serialize(self):
        schema = DebtItemSchema()
        return schema.dump(self).data

    @classmethod
    def from_json(cls, data):
        schema = DebtItemSchema()
        schema.load(data)
        return cls(**data)
