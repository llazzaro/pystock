"""add foreign keys after table rename

Revision ID: 34932a78ed85
Revises: 727cf9f18be
Create Date: 2014-10-04 01:07:41.226006

"""

# revision identifiers, used by Alembic.
revision = '34932a78ed85'
down_revision = '727cf9f18be'

from alembic import op


def upgrade():
    op.create_foreign_key("pystock_trade_security_id_fkey", "pystock_trade", "pystock_security", ["security_id"], ["id"])
    op.create_unique_constraint(u'security_register_number_key', 'pystock_trade', ['security_id', 'trade_date', 'register_number'])

    op.create_unique_constraint('pystock_exchange_unique_code', 'pystock_exchange', ['code'])


def downgrade():
    op.drop_constraint('pystock_trade_security_id_fkey', 'pystock_trade', type="foreignkey")
    op.drop_constraint('security_register_number_key', 'pystock_trade')
    op.drop_constraint('pystock_exchange_unique_code', 'pystock_exchange')
