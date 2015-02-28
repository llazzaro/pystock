"""fix adr and rename price in trade

Revision ID: 32e0f77a282f
Revises: 50e1ac18dab6
Create Date: 2015-02-28 00:26:32.708532

"""

# revision identifiers, used by Alembic.
revision = '32e0f77a282f'
down_revision = '182e944eaf02'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column("pystock_split", "asset_id", name="security_id")
    op.alter_column("pystock_dividend", "asset_id", name="security_id")

    op.create_table('pystock_adr',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('security_id', sa.Integer(), nullable=True),
        sa.Column('adr_security_id', sa.Integer(), nullable=True),
        sa.Column('exchange_id', sa.Integer(), nullable=True),
        sa.Column('ratio', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.drop_column(u'pystock_stock', 'adr_id')


def downgrade():
    op.drop_table('pystock_adr')
    op.alter_column("pystock_dividend", "security_id", name="asset_id")
    op.alter_column("pystock_split", "security_id", name="asset_id")
