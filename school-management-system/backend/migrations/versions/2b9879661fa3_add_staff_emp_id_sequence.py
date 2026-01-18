"""add staff emp_id sequence

Revision ID: 2b9879661fa3
Revises: 3795ef328391
Create Date: 2026-01-18 19:06:23.092536

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b9879661fa3'
down_revision = '3795ef328391'
branch_labels = None
depends_on = None


def upgrade():
     op.execute(
        """
        CREATE SEQUENCE IF NOT EXISTS staff_emp_id_seq
        START WITH 1
        INCREMENT BY 1
        NO MINVALUE
        NO MAXVALUE
        CACHE 1;
        """
    )


def downgrade():
    pass
