
from datetime import datetime
from typing import List
from pydantic import BaseModel
from ..models.common import SubTypeEnum


class SubscriptionBase(BaseModel):
    user_identifier: str
    sub_type: SubTypeEnum
    sub_address: str
    is_active: bool | None = True
    meta_flag: str | None = None


class Subscription(SubscriptionBase):
    id: int
    create_time: datetime
    update_time: datetime

    class Config:
        from_attributes = True


class UnsubscribeSchema(BaseModel):
    user_identifier: str | None = None
    email: str | None = None
    mobile: str | None = None


class RespBaseSchema(BaseModel):
    msg: str
    err_code: str


class RespSubSchema(RespBaseSchema):
    data: Subscription


class RespMultiSubSchema(RespBaseSchema):
    data: List[Subscription]


class RespUnsubSchema(RespBaseSchema):
    data: List[int]
