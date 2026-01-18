"""add revoked_token table

Revision ID: cf4540c63fc0
Revises: 32264761a16c
Create Date: 2026-01-18 05:16:20.710970
"""

from alembic import op
import sqlalchemy as sa


revision = "cf4540c63fc0"
down_revision = "32264761a16c"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "revoked_token",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("jti", sa.String(length=36), nullable=False, unique=True),
        sa.Column("reason", sa.String(length=255)),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )


def downgrade():
    op.drop_table("revoked_token")
