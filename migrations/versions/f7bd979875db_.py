"""empty message

Revision ID: f7bd979875db
Revises: 4308d719b6c2
Create Date: 2024-01-21 01:39:54.782579

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f7bd979875db'
down_revision: Union[str, None] = '4308d719b6c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
