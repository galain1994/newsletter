
from datetime import datetime
from pydantic import BaseModel
from ..common import SubTypeEnum


class SubscriptionBase(BaseModel):
    user_identifier: str
    sub_type: SubTypeEnum
    sub_address: str
    is_active: bool | None = True
    meta_flag: str | None = None


class SubscriptionCreate(SubscriptionBase):

    pass

class Subscription(SubscriptionBase):
    id: int
    create_time: datetime
    update_time: datetime

    class Config:
        from_attributes = True
