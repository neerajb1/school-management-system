"""add onboarding fields to user_account

Revision ID: 3795ef328391
Revises: 80c3d0169931
Create Date: 2026-01-18 16:53:07.819546

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3795ef328391'
down_revision = '80c3d0169931'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Add full_name (nullable first for safety)
    op.add_column(
        "user_account",
        sa.Column("full_name", sa.String(length=255), nullable=True)
    )

    # 2. Add phone
    op.add_column(
        "user_account",
        sa.Column("phone", sa.String(length=20), nullable=True)
    )

    # 3. Add account_status with server default
    op.add_column(
        "user_account",
        sa.Column(
            "account_status",
            sa.String(length=32),
            nullable=False,
            server_default="ACTIVE"
        )
    )

    # 4. Backfill full_name for existing users
    op.execute(
        """
        UPDATE user_account
        SET full_name = email
        WHERE full_name IS NULL
        """
    )

    # 5. Enforce NOT NULL after backfill
    op.alter_column(
        "user_account",
        "full_name",
        nullable=False
    )

    # 6. Remove server default (let app control it)
    op.alter_column(
        "user_account",
        "account_status",
        server_default=None
    )



def downgrade():
    pass
