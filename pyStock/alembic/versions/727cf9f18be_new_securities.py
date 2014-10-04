"""new securities

Revision ID: 727cf9f18be
Revises: 3a5095ddf365
Create Date: 2014-10-04 01:06:01.242863

"""

# revision identifiers, used by Alembic.
revision = '727cf9f18be'
down_revision = '3a5095ddf365'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('pystock_stock',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('company_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['company_id'], ['pystock_company.id'], ),
        sa.ForeignKeyConstraint(['id'], ['pystock_security.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('pystock_bond',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['id'], ['pystock_security.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('pystock_asset',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['id'], ['pystock_security.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('pystock_bond')
    op.drop_table('pystock_stock')
