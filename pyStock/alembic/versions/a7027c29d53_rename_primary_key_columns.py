""" rename primary key columns

Revision ID: a7027c29d53
Revises: c64d60d6875
Create Date: 2015-01-10 10:58:35.258682

"""

# revision identifiers, used by Alembic.
revision = 'a7027c29d53'
down_revision = 'c64d60d6875'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.rename_table('pystock_canceled_order', 'pystock_cancel_order')
    op.rename_table('pystock_filled_order', 'pystock_fill_order')
    op.alter_column("pystock_open_order", "open_id", name="id")
    op.alter_column("pystock_fill_order", "filled_id", name="id")
    op.alter_column("pystock_cancel_order", "cancel_id", name="id")
    op.add_column(u'pystock_order', sa.Column('security_id', sa.Integer(), nullable=True))


def downgrade():
    pass
