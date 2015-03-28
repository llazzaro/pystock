"""new orders migration

Revision ID: 3dabdfc80427
Revises: 46b0851df7e5
Create Date: 2015-03-28 15:25:04.797810

"""

# revision identifiers, used by Alembic.
revision = '3dabdfc80427'
down_revision = '46b0851df7e5'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('pystock_buy_to_cover_order',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('pystock_sell_short_order',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    pass
