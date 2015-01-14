""" reification of orders again

Revision ID: 3697e57b1a31
Revises: 45eb7b55c507
Create Date: 2015-01-11 15:51:54.101000

"""

# revision identifiers, used by Alembic.
revision = '3697e57b1a31'
down_revision = '45eb7b55c507'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_table('pystock_cancel_order')
    op.drop_table('pystock_closed_order')
    op.drop_table('pystock_fill_order')
    op.drop_table('pystock_open_order')
    op.drop_column(u'pystock_order', 'next_step_id')
    op.add_column(u'pystock_order', sa.Column('stage_id', sa.Integer(), nullable=False))

    op.create_table('pystock_buy_order',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table('pystock_sell_order',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_foreign_key("pystock_sell_order_polymorphic_fkey", "pystock_order", "pystock_sell_order", ["id"], ["id"])
    op.create_foreign_key("pystock_buy_order_polymorphic_fkey", "pystock_order", "pystock_buy_order", ["id"], ["id"])

    op.create_table('pystock_stage_order',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.Column('executed_on', sa.DateTime(), nullable=True),
        sa.Column('next_stage', sa.Integer(), nullable=True),
        sa.Column('stage_type', sa.String(), nullable=True),
    )

    op.create_table('pystock_open_stage_order',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_foreign_key("pystock_open_stage_order_polymorphic_fkey", "pystock_stage_order", "pystock_open_stage_order", ["id"], ["id"])

    op.create_table('pystock_fill_stage_order',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_foreign_key("pystock_fill_stage_order_polymorphic_fkey", "pystock_stage_order", "pystock_fill_stage_order", ["id"], ["id"])

    op.create_table('pystock_cancel_stage_order',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_foreign_key("pystock_cancel_stage_order_polymorphic_fkey", "pystock_stage_order", "pystock_cancel_stage_order", ["id"], ["id"])


def downgrade():
    pass
