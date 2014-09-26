"""Reification of security

Revision ID: 1bdff1c4e687
Revises: 2c08fb5b6e72
Create Date: 2014-09-09 23:28:33.495896

"""

# revision identifiers, used by Alembic.
revision = '1bdff1c4e687'
down_revision = '3bfca079f84d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # drop foreign to change the table/column name
    op.drop_constraint('pystock_tick_asset_id_fkey', 'pystock_tick', type="foreignkey")
    op.drop_constraint('asset_register_number_key', 'pystock_tick')
    op.alter_column("pystock_tick", "asset_id", name="security_id")
    op.rename_table('pystock_asset', 'pystock_security')
    op.create_foreign_key("pystock_tick_security_id_fkey", "pystock_tick", "pytstock_security", ["security_id"], ["id"])
    op.create_unique_constraint(u'security_register_number_key', 'pystock_tick', ['security_id', 'tick_date', 'register_number'])

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
    op.drop_constraint('pystock_tick_security_id_fkey', 'pystock_tick', type="foreignkey")
    op.drop_constraint('security_register_number_key', 'pystock_tick')
    op.alter_column("pystock_tick", "security_id", name="asset_id")
    op.rename_table('pystock_security', 'pystock_asset')
    op.create_foreign_key("pystock_tick_asset_id_fkey", "pystock_tick", "pytstock_asset", ["asset_id"], ["id"])
    op.create_unique_constraint(u'asset_register_number_key', 'pystock_tick', ['asset_id', 'tick_date', 'register_number'])
    op.drop_table('pystock_stock')
    op.drop_table('pystock_bond')
