""" remove fkey on joined table inheritance

Revision ID: 39320aca87a2
Revises: a7027c29d53
Create Date: 2015-01-10 11:15:47.028799

"""

# revision identifiers, used by Alembic.
revision = '39320aca87a2'
down_revision = 'a7027c29d53'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_constraint('pystock_order_open_order_polymorphic_fkey', 'pystock_order', type="foreignkey")
    op.drop_constraint('pystock_order_filled_order_polymorphic_fkey', 'pystock_order', type="foreignkey")
    op.drop_constraint('pystock_order_canceled_order_polymorphic_fkey', 'pystock_order', type="foreignkey")


def downgrade():
    pass
