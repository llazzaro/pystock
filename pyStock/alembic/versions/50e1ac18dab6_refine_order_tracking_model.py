""" refine order tracking model

Revision ID: 50e1ac18dab6
Revises: 2799a1e62787
Create Date: 2015-02-02 15:21:43.045116

"""

# revision identifiers, used by Alembic.
revision = '50e1ac18dab6'
down_revision = '2799a1e62787'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_table('pystock_close_stage_order')
    op.create_table('pystock_order_tracking',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('share', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    pass
