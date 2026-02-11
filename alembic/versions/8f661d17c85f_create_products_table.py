"""create products table

Revision ID: 8f661d17c85f
Revises: f3070d45e4ea
Create Date: 2026-02-09 16:44:46.444293

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8f661d17c85f'
down_revision: Union[str, Sequence[str], None] = 'f3070d45e4ea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
