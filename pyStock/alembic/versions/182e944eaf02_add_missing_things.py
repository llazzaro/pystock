""" add missing things

Revision ID: 182e944eaf02
Revises: 50e1ac18dab6
Create Date: 2015-02-24 21:53:11.133108

"""

# revision identifiers, used by Alembic.
revision = '182e944eaf02'
down_revision = '50e1ac18dab6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(u'pystock_order_tracking', sa.Column('buy_order_id', sa.Integer(), nullable=False))
    op.add_column(u'pystock_order_tracking', sa.Column('sell_order_id', sa.Integer(), nullable=False))
    op.create_foreign_key("pystock_tracking_sell_id_fkey", "pystock_order_tracking", "pystock_sell_order", ["sell_order_id"], ["id"])
    op.create_foreign_key("pystock_tracking_buy_id_fkey", "pystock_order_tracking", "pystock_buy_order", ["buy_order_id"], ["id"])



def downgrade():
    pass
