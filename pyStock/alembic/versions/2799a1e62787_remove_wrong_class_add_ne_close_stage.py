""" remove wrong class add ne close stage

Revision ID: 2799a1e62787
Revises: 371fb70d84c6
Create Date: 2015-01-29 23:03:08.261208

"""

# revision identifiers, used by Alembic.
revision = '2799a1e62787'
down_revision = '371fb70d84c6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('pystock_close_stage_order',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('price', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    pass
