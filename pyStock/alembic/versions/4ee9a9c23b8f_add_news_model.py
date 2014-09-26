"""Add news model

Revision ID: 4ee9a9c23b8f
Revises: 1bdff1c4e687
Create Date: 2014-09-10 16:21:43.655828

"""

# revision identifiers, used by Alembic.
revision = '4ee9a9c23b8f'
down_revision = '1bdff1c4e687'

from alembic import op
import sqlalchemy as sa


def upgrade():

    op.create_table('pystock_news_source',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('pystock_news',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('news_source_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['news_source_id'], ['pystock_news_source.id'], ),
        sa.Column('symbol', sa.String(), nullable=True),
        sa.Column('information', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('pystock_news')
    op.drop_table('pystock_news_source')
