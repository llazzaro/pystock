""" add polymorpic_on for security

Revision ID: 342abc30c977
Revises: 34932a78ed85
Create Date: 2014-10-04 12:09:11.563435

"""

# revision identifiers, used by Alembic.
revision = '342abc30c977'
down_revision = '34932a78ed85'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(u'pystock_security', sa.Column('security_type', sa.String(), nullable=True))


def downgrade():
    op.drop_column(u'pystock_security', sa.Column('security_type', sa.String(), nullable=True))
