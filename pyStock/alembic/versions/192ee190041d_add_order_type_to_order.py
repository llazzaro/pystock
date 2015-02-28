""" add order_type to order

Revision ID: 192ee190041d
Revises: 7d142f25e30
Create Date: 2015-01-05 23:42:48.820150

"""

# revision identifiers, used by Alembic.
revision = '192ee190041d'
down_revision = '45eb7b55c507'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(u'pystock_order', sa.Column('order_type', sa.String(), nullable=True))


def downgrade():
    pass
