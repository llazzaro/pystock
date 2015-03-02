"""rename columns in order

Revision ID: 586f897f719
Revises: 32e0f77a282f
Create Date: 2015-02-28 15:53:54.383325

"""

# revision identifiers, used by Alembic.
revision = '586f897f719'
down_revision = '32e0f77a282f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column("pystock_order", "price", name="_price")
    op.alter_column("pystock_order", "share", name="_shares")


def downgrade():
    op.alter_column("pystock_order", "_price", name="price")
    op.alter_column("pystock_order", "_shares", name="share")
