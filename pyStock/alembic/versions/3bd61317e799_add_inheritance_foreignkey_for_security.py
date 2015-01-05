""" add inheritance foreignkey for security

Revision ID: 3bd61317e799
Revises: 342abc30c977
Create Date: 2014-10-04 12:17:09.476387

"""

# revision identifiers, used by Alembic.
revision = '3bd61317e799'
down_revision = '342abc30c977'

from alembic import op


def upgrade():
    op.create_foreign_key("pystock_stock_id_security_id_polymorphic_fkey", "pystock_stock", "pystock_security", ["id"], ["id"])
    op.create_foreign_key("pystock_bond_id_security_id_polymorphic_fkey", "pystock_bond", "pystock_security", ["id"], ["id"])
    op.create_foreign_key("pystock_asset_id_security_id_polymorphic_fkey", "pystock_asset", "pystock_security", ["id"], ["id"])


def downgrade():
    op.drop_constraint('pystock_stock_id_security_id_polymorphic_fkey', 'pystock_stock', type="foreignkey")
    op.drop_constraint('pystock_bond_id_security_id_polymorphic_fkey', 'pystock_bond', type="foreignkey")
    op.drop_constraint('pystock_asset_id_security_id_polymorphic_fkey', 'pystock_asset', type="foreignkey")
