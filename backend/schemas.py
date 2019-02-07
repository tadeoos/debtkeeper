from datetime import date
from marshmallow import Schema, fields, pprint


class DebtItemSchema(Schema):
    kind = fields.Str()
    due_date = fields.Date()
    created = fields.DateTime()
    who = fields.Str()
    what = fields.Str()
    resolved = fields.Bool()
