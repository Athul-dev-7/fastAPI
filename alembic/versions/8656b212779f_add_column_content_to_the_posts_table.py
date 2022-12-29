"""add column content to the posts table

Revision ID: 8656b212779f
Revises: fcdf133c0bdb
Create Date: 2022-12-29 10:34:29.574493

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8656b212779f"
down_revision = "fcdf133c0bdb"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")
