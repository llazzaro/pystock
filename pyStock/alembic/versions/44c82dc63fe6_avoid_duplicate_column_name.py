""" avoid duplicate column name

Revision ID: 44c82dc63fe6
Revises: 166bcdc0e706
Create Date: 2015-01-05 23:58:55.673299

"""

# revision identifiers, used by Alembic.
revision = '44c82dc63fe6'
down_revision = '166bcdc0e706'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column("pystock_open_order", "id", name="open_id")
    op.alter_column("pystock_closed_order", "id", name="close_id")
    op.alter_column("pystock_filled_order", "id", name="filled_id")
    op.alter_column("pystock_canceled_order", "id", name="cancel_id")


def downgrade():
    pass
