"""remove news model

Revision ID: 4f8d5dcf17a0
Revises: 2555a49d58a3
Create Date: 2015-01-05 21:55:49.014212

"""

# revision identifiers, used by Alembic.
revision = '4f8d5dcf17a0'
down_revision = '2555a49d58a3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_table('pystock_news')
    op.drop_table('pystock_news_source')


def downgrade():
    pass
