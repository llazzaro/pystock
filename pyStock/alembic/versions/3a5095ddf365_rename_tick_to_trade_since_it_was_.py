"""rename tick to trade, since it was actually a trade

Revision ID: 3a5095ddf365
Revises: 55126c331f54
Create Date: 2014-09-26 16:52:15.490819

"""

# revision identifiers, used by Alembic.
revision = '3a5095ddf365'
down_revision = '55126c331f54'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.rename_table('pystock_tick', 'pystock_trade')
    op.alter_column("pystock_trade", "tick_date", name="trade_date")


def downgrade():
    op.rename_table('pystock_trade', 'pystock_tick')
    op.alter_column("pystock_tick", "trade_date", name="tick_date")
