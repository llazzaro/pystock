""" reification orders

Revision ID: 33701ee2c2b9
Revises: 4f8d5dcf17a0
Create Date: 2015-01-05 23:14:05.534376

"""

# revision identifiers, used by Alembic.
revision = '33701ee2c2b9'
down_revision = '4f8d5dcf17a0'

from alembic import op
import sqlalchemy as sa


def upgrade():

    op.create_table('pystock_open_order',
        sa.Column('open_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.Column('open_on', sa.DateTime(), nullable=True),
    )

    op.create_table('pystock_canceled_order',
        sa.Column('cancel_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.Column('canceled_on', sa.DateTime(), nullable=True),
    )

    op.create_table('pystock_filled_order',
        sa.Column('filled_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.Column('filled_on', sa.DateTime(), nullable=True),
    )

    op.create_table('pystock_closed_order',
        sa.Column('close_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.Column('closed_on', sa.DateTime(), nullable=True),
    )
    op.create_foreign_key("pystock_order_open_order_polymorphic_fkey", "pystock_order", "pystock_open_order", ["id"], ["open_id"])
    op.create_foreign_key("pystock_order_canceled_order_polymorphic_fkey", "pystock_order", "pystock_canceled_order", ["id"], ["cancel_id"])
    op.create_foreign_key("pystock_order_filled_order_polymorphic_fkey", "pystock_order", "pystock_filled_order", ["id"], ["filled_id"])
    op.create_foreign_key("pystock_order_cloed_order_polymorphic_fkey", "pystock_order", "pystock_closed_order", ["id"], ["closed_id"])


def downgrade():
    pass
