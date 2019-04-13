import datetime

from passlib.context import CryptContext
from pony import orm

from schemas import DebtItemOut


def define_entities(db):

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    class User(db.Entity):

        _table_ = 'users'

        name = orm.Required(str, unique=True)
        email = orm.Optional(str)
        password = orm.Required(str)
        debts = orm.Set("DebtItem")
        created = orm.Optional(datetime.datetime)

        def before_insert(self):
            self.password = pwd_context.hash(self.password)
            self.created = datetime.datetime.now()

        def get_serialized_debts(self, **kwargs):
            resolved_values = kwargs.get('resolved', [True, False])
            kind_values = kwargs.get('kind', ['loan', 'debt'])
            debts = self.debts.select(
                lambda d: d.resolved in resolved_values and d.kind in kind_values
            ).order_by(DebtItem.resolved, DebtItem.created)
            return [debt_item.serialize() for debt_item in debts]

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
            if BlacklistToken.get(token=auth_token):
                raise ValueError("Token blacklisted.")
            return True

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
            schema = DebtItemOut(**self.to_dict())
            return schema.dict()


def define_database(**db_params):
    db = orm.Database(**db_params)
    define_entities(db)
    db.generate_mapping(create_tables=True)
    return db
