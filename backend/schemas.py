from datetime import (
    date,
    datetime,
)

from pydantic import BaseModel


class DebtItemSchema(BaseModel):
    kind: str
    due_date: date
    created: datetime
    who: str
    what: str
    resolved: bool


class UserSchema(BaseModel):
    name: str
