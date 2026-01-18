"""add user_account mapping to student and guardian

Revision ID: 1683202d6e58
Revises: 2b9879661fa3
Create Date: 2026-01-18 20:52:52.227986

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1683202d6e58'
down_revision = '2b9879661fa3'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("student") as batch_op:
        batch_op.add_column(
            sa.Column(
                "user_account_id",
                sa.BigInteger(),
                sa.ForeignKey("user_account.id"),
                nullable=True,
            )
        )
        batch_op.create_unique_constraint(
            "uq_student_user_account",
            ["user_account_id"]
        )

    with op.batch_alter_table("guardian") as batch_op:
        batch_op.add_column(
            sa.Column(
                "user_account_id",
                sa.BigInteger(),
                sa.ForeignKey("user_account.id"),
                nullable=True,
            )
        )
        batch_op.create_unique_constraint(
            "uq_guardian_user_account",
            ["user_account_id"]
        )


def downgrade():
    pass
