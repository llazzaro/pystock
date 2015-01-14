""" add fkey to bond

Revision ID: 45eb7b55c507
Revises: 39320aca87a2
Create Date: 2015-01-10 12:45:37.155229

"""

# revision identifiers, used by Alembic.
revision = '45eb7b55c507'
down_revision = '39320aca87a2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_foreign_key("pystock_trade_bond_id_fkey", "pystock_bond", "pystock_security", ["id"], ["id"])


def downgrade():
    pass
