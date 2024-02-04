
from datetime import datetime
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


class Unsubscription(BaseModel):
    user_identifier: str | None = None
    email: str | None = None
    mobile: str | None = None
