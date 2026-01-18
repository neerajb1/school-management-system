"""add student admission number sequence

Revision ID: 1f403601fc90
Revises: 1683202d6e58
Create Date: 2026-01-18 23:03:46.418403

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f403601fc90'
down_revision = '1683202d6e58'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        CREATE SEQUENCE IF NOT EXISTS student_admission_seq
        START WITH 1
        INCREMENT BY 1
        MINVALUE 1
        OWNED BY NONE
        """
    )



def downgrade():
    pass
