

from datetime import datetime
import sqlalchemy as sa
from .base import Base
from ..common import SubTypeEnum
from ..schemas.subscription import SubscriptionCreate, SubscriptionBase


class Subscription(Base):
    """
    Newsletter Subscription model based on user identifier provided by external system, could be uuid.
    `订阅`模型, user_identifier 取自统一用户中心或另一张用户表, 可以是uuid.
    """
    __tablename__ = 'subscription'
    __table_args__ = (
        sa.UniqueConstraint('sub_type', 'sub_address', name='sub_type_sub_address_uix'),
    )

    # ID
    id = sa.Column(
        'id', sa.Integer,
        primary_key=True, comment="ID"
    )
    # User identifier
    user_identifier = sa.Column(
        'user_identifier', sa.String(64), index=True, nullable=False,
        comment='User Identifier'
    )
    # Subscription type from `SubTypeEnum`
    sub_type = sa.Column(
        'sub_type', sa.Enum(SubTypeEnum), nullable=False, comment="Subscription Type"
    )
    # Email, mobile or other type decided by sub_type 具体含义取决于sub_type, 可以是邮箱或手机号
    sub_address = sa.Column(
        'sub_address', sa.String(256), nullable=False, comment="Subscription Address"
    )
    # Is actively subscribed
    is_active = sa.Column(
        'is_active', sa.Boolean, index=True, default=True,
        comment="Is active"
    )
    # Meta Data
    create_time = sa.Column(
        'create_time', sa.TIMESTAMP, default=sa.ColumnDefault(datetime.utcnow),
        comment="Create Timestamp"
    )
    update_time = sa.Column(
        'update_time', sa.TIMESTAMP, default=sa.ColumnDefault(datetime.utcnow),
        comment="Update Timestamp"
    )
    # Reserved column to indicate where data comes from
    meta_flag = sa.Column(
        'meta_flag', sa.String, comment="Meta Flag"
    )

    @classmethod
    def create_subscription(cls, db_session: sa.orm.session.Session, data: SubscriptionCreate):
        """Create Subscription"""
        obj = cls(**data.model_dump())
        db_session.add(obj)
        db_session.commit()
        return obj

    @classmethod
    def create_or_update_subscription(cls, db_session: sa.orm.session.Session, data: SubscriptionBase):
        """Create or update subscription based on sub_type and user"""
        record = db_session.execute(sa.select(cls).filter_by(
            user_identifier=data.user_identifier, sub_type=data.sub_type
        )).scalar_one()

        if not record:
            record = cls.create_subscription(db_session, data)
        else:
            import pdb; pdb.set_trace()
            record.update_subscription(db_session, data)
        return record

    def update_subscription(self, db_session: sa.orm.session.Session, data: SubscriptionBase):
        """Update subscription"""
        import pdb; pdb.set_trace()
        self.update(data.model_dump(), update_time=datetime.utcnow())
        db_session.commit()
