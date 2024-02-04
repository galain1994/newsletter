

from datetime import datetime
import sqlalchemy as sa
from .base import Base
from .common import SubTypeEnum


class Subscription(Base):
    """
    Newsletter Subscription model based on user identifier provided by external system, could be uuid.
    `订阅`模型, user_identifier 取自统一用户中心或另一张用户表, 可以是uuid.
    """
    __tablename__ = 'subscription'
    __table_args__ = (
        sa.UniqueConstraint('user_identifier', 'sub_type', name='user_sub_type_uix'),
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
