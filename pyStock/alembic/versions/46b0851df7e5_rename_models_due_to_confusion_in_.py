"""rename models due to confusion in definitions

Revision ID: 46b0851df7e5
Revises: 2a3018360daa
Create Date: 2015-03-16 22:14:48.901691

"""

# revision identifiers, used by Alembic.
revision = '46b0851df7e5'
down_revision = '2a3018360daa'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_table('pystock_quote')
    op.rename_table('pystock_trade', 'pystock_tick')
    op.rename_table('pystock_historical', 'pystock_quote')
    op.rename_table('pystock_exchange_historical', 'pystock_exchange_quote')
    op.rename_table('pystock_security_historical', 'pystock_security_quote')


def downgrade():
    pass
