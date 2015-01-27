""" add adr relation

Revision ID: 371fb70d84c6
Revises: 168829b75572
Create Date: 2015-01-25 21:40:16.015665

"""

# revision identifiers, used by Alembic.
revision = '371fb70d84c6'
down_revision = '168829b75572'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(u'pystock_stock', sa.Column('adr_id', sa.Integer(), nullable=True))


def downgrade():
    pass
