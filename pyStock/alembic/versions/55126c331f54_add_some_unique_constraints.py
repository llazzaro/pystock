"""add some unique constraints

Revision ID: 55126c331f54
Revises: 2c08fb5b6e72
Create Date: 2014-09-26 00:50:26.256428

"""

# revision identifiers, used by Alembic.
revision = '55126c331f54'
down_revision = '2c08fb5b6e72'

from alembic import op


def upgrade():
    op.create_unique_constraint(None, 'pystock_currency', ['code'])
    op.create_index('unique_monetary_date', 'pystock_fxrate', ['date', 'monetary_source_id'], unique=True)
    op.create_unique_constraint(u'unique_monetary_date', 'pystock_fxrate', ['date', 'monetary_source_id'])
    op.create_unique_constraint(None, 'pystock_exchange', ['code'])
    op.create_foreign_key("pystock_security_exchange_id_fkey", "pystock_security", "pytstock_exchange", ["exchange_id"], ["id"])


def downgrade():
    op.drop_constraint(None, 'pystock_currency')
    op.drop_constraint(None, 'unique_monetary_date')
    op.drop_constraint(None, 'pystock_exchange')

