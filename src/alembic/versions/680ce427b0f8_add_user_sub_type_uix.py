"""Add user_sub_type_uix

Revision ID: 680ce427b0f8
Revises: 69b942ff6dcb
Create Date: 2024-02-04 20:33:15.500824

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '680ce427b0f8'
down_revision: Union[str, None] = '69b942ff6dcb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
