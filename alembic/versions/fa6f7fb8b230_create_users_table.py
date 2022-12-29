"""create users table

Revision ID: fa6f7fb8b230
Revises: 8656b212779f
Create Date: 2022-12-29 10:42:48.116388

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.sql.sqltypes


# revision identifiers, used by Alembic.
revision = "fa6f7fb8b230"
down_revision = "8656b212779f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )


def downgrade() -> None:
    op.drop_table("users")
