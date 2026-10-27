"""Create phone number for users

Revision ID: d3ca378ed88c
Revises:
Create Date: 2026-08-17 15:34:57.202120

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'd3ca378ed88c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""

    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))

def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column('users', 'phone_number')
