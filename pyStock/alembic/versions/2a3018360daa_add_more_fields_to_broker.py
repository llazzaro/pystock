"""add more fields to broker

Revision ID: 2a3018360daa
Revises: 586f897f719
Create Date: 2015-03-04 00:17:46.337871

"""

# revision identifiers, used by Alembic.
revision = '2a3018360daa'
down_revision = '586f897f719'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(u'pystock_broker', sa.Column('cateogry', sa.String(), nullable=True))
    op.add_column(u'pystock_broker', sa.Column('web', sa.String(), nullable=True))
    op.add_column(u'pystock_broker', sa.Column('email', sa.String(), nullable=True))


def downgrade():
    pass
