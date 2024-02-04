

from typing import Optional, List
from datetime import datetime
from sqlalchemy import and_, or_
from sqlalchemy.orm import session as sa_session, query as sa_query
from ..models.common import SubTypeEnum
from ..models.subscription import Subscription
from ..schemas.subscription import SubscriptionBase, Subscription as SubscriptionSchema


def check_email(email: str):
    """Check if valid email address"""
    pass


def check_mobile(mobile: str):
    """Check if valid mobile number"""
    pass


def search_subscription(
        db_session: sa_session.Session,
        user_identifier: Optional[str], email: Optional[str], mobile: Optional[str]
    ):
    """Search Database subscriptions by user_identifier, mobile or email
    根据用户/email/手机号搜索订阅详情

    :param db_session: database session
    :type db_session: sa_session.Session
    :param user_identifier: search subscription by user_identifier
    :type user_identifier: Optional[str]
    :param email: search subscription by email
    :type email: Optional[str]
    :param mobile: search subscription by mobile
    :type mobile: Optional[str]
    """
    if user_identifier:
        records = db_session.query(Subscription).filter(
            and_(
                Subscription.user_identifier == user_identifier,
            )
        ).all()
    elif email or mobile:
        records = db_session.query(Subscription).filter(
            or_(
                and_(
                    Subscription.sub_type == SubTypeEnum.email,
                    Subscription.sub_address == email
                ),
                and_(
                    Subscription.sub_type == SubTypeEnum.sns,
                    Subscription.sub_address == mobile
                )
            )
        ).all()
    else:
        records = []
    return records
    

def create_subscription(db_session: sa_session.Session, data: SubscriptionBase):
    """Create Subscription"""
    # TODO: validate email or mobile according to sub_type 根据sub_type判断email和mobile合法性
    obj = Subscription(**data.model_dump())
    db_session.add(obj)
    db_session.commit()
    SubscriptionSchema.model_validate(obj)
    return obj


def update_subscription(query: sa_query.Query, db_session: sa_session.Session, data: SubscriptionBase):
    """Update subscription"""
    instance = query.scalar()
    _update = False
    for _field in data.model_fields:
        if getattr(instance, _field, None) != getattr(data, _field):
            _update = True
            break
    if _update:
        updates = data.model_dump()
        updates['update_time'] = datetime.utcnow()
        query.update(updates)
        db_session.commit()


def create_or_update_subscription(db_session: sa_session.Session, data: SubscriptionBase):
    """Create or update subscription based on sub_type and user"""
    query = db_session.query(Subscription).filter(
        Subscription.user_identifier == data.user_identifier,
        Subscription.sub_type == data.sub_type
    )
    if not query.scalar():
        record = create_subscription(db_session, data)
    else:
        update_subscription(query, db_session, data)
        record = query.scalar()
    return record


def unsubscribe(db_session: sa_session.Session, subscriptions: List[Subscription]):
    """Unsubscribe by subscription list"""
    for subscription in subscriptions:
        db_session.query(Subscription).filter(
            Subscription.id == subscription.id
        ).update({'is_active': False})
    db_session.commit()
