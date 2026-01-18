"""add refresh_token table

Revision ID: 2a1dd27b4a8f
Revises: cf4540c63fc0
Create Date: 2026-01-18 13:43:50.719426

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a1dd27b4a8f'
down_revision = 'cf4540c63fc0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "refresh_token",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, nullable=False, index=True),
        sa.Column("jti", sa.String(length=255), nullable=False, unique=True),
        sa.Column("expires_at", sa.DateTime, nullable=False),
        sa.Column(
            "is_revoked",
            sa.Boolean,
            nullable=False,
            server_default=sa.false(),
        ),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
        sa.Column("created_by_id", sa.Integer, nullable=True),
        sa.Column("updated_by_id", sa.Integer, nullable=True),
    )



def downgrade():
    pass
