""" add owner to account

Revision ID: c64d60d6875
Revises: 44c82dc63fe6
Create Date: 2015-01-06 00:09:47.198247

"""

# revision identifiers, used by Alembic.
revision = 'c64d60d6875'
down_revision = '44c82dc63fe6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(u'pystock_account', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.create_foreign_key("pystock_account_owner_id_fkey", "pystock_account", "pystock_owner", ["owner_id"], ["id"])


def downgrade():
    pass
