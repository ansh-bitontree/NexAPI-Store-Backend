"""create products table

Revision ID: f3070d45e4ea
Revises: 3b859d9acea5
Create Date: 2026-02-09 15:37:19.774359
"""
from alembic import op
import sqlalchemy as sa
from typing import Union, Sequence

# revision identifiers, used by Alembic.
revision: str = 'f3070d45e4ea'
down_revision: Union[str, Sequence[str], None] = '3b859d9acea5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create products table"""
    op.create_table(
        "products",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("price", sa.Integer, nullable=False),
        sa.Column("discount_percentage", sa.Float, default=0.0),
        sa.Column("quantity", sa.Integer, default=0),
        sa.Column("category", sa.String(100), index=True),
        sa.Column("brand", sa.String(100)),
        sa.Column("image_url", sa.String(500)),
        sa.Column("rating", sa.Float, default=0.0),
        sa.Column("created_at", sa.DateTime, nullable=True),
        sa.Column("is_active", sa.Boolean, default=True),
    )


def downgrade() -> None:
    """Drop products table"""
    op.drop_table("products")
