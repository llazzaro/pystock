""" add historical

Revision ID: f589bff6f63
Revises: 3697e57b1a31
Create Date: 2015-01-15 14:18:41.340854

"""

# revision identifiers, used by Alembic.
revision = 'f589bff6f63'
down_revision = '3697e57b1a31'

from alembic import op
import sqlalchemy as sa


def upgrade():

    op.create_table('pystock_historical',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('close_price', sa.DECIMAL(), nullable=False),
        sa.Column('high_price', sa.DECIMAL(), nullable=False),
        sa.Column('low_price', sa.DECIMAL(), nullable=False),
        sa.Column('open_price', sa.DECIMAL(), nullable=False),
        sa.Column('unadj', sa.DECIMAL(), nullable=False),
        sa.Column('volume', sa.DECIMAL(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('pystock_exchange_historical',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('exchange_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['exchange_id'], ['pystock_exchange.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('pystock_security_historical',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('security_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['security_id'], ['pystock_security.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    pass
