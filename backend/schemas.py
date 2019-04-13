from datetime import (
    date,
    datetime,
)

from pydantic import BaseModel


class BaseDebtItem(BaseModel):
    kind: str
    who: str
    what: str
    due_date: date


class DebtItemIn(BaseDebtItem):
    resolved: bool = False


class DebtItemOut(BaseDebtItem):
    id: int
    resolved: bool
    created: datetime


class DebtItemPatch(BaseModel):
    resolved: bool


class UserSchema(BaseModel):
    name: str
