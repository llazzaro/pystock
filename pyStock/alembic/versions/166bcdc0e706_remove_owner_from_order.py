""" remove owner from order

Revision ID: 166bcdc0e706
Revises: 192ee190041d
Create Date: 2015-01-05 23:46:53.887023

"""

# revision identifiers, used by Alembic.
revision = '166bcdc0e706'
down_revision = '192ee190041d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column(u'pystock_order', 'owner_id')
    pass


def downgrade():
    pass
