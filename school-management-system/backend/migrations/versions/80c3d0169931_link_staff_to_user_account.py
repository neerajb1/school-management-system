"""link staff to user_account

Revision ID: 80c3d0169931
Revises: 2a1dd27b4a8f
Create Date: 2026-01-18 16:51:54.733382

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80c3d0169931'
down_revision = '2a1dd27b4a8f'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Add column
    op.add_column(
        "staff",
        sa.Column(
            "user_account_id",
            sa.BigInteger(),
            nullable=True
        )
    )

    # 2. Foreign key
    op.create_foreign_key(
        "fk_staff_user_account",
        "staff",
        "user_account",
        ["user_account_id"],
        ["id"]
    )

    # 3. One-to-one constraint
    op.create_unique_constraint(
        "uq_staff_user_account",
        "staff",
        ["user_account_id"]
    )



def downgrade():
    pass
