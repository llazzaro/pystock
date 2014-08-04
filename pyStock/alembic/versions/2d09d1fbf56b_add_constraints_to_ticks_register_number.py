"""add constraints to ticks register number

Revision ID: 2d09d1fbf56b
Revises: 7d0cfaec4a0
Create Date: 2014-08-03 22:20:18.278034

"""

# revision identifiers, used by Alembic.
revision = '2d09d1fbf56b'
down_revision = '7d0cfaec4a0'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute("ALTER TABLE pystock_tick ADD CONSTRAINT register_number_key UNIQUE (register_number);")


def downgrade():
    pass
