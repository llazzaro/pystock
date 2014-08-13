"""add constraints to ticks register number

Revision ID: 2d09d1fbf56b
Revises: 7d0cfaec4a0
Create Date: 2014-08-03 22:20:18.278034

"""

# revision identifiers, used by Alembic.
revision = '2d09d1fbf56b'
down_revision = '7d0cfaec4a0'

from alembic import op


def upgrade():
    op.execute("""
            DELETE
            FROM pystock_tick
            WHERE id NOT IN (
               SELECT MIN(id) as id
               FROM pystock_tick
               GROUP BY asset_id, tick_date, register_number
            )
    """)
    op.execute("ALTER TABLE pystock_tick ADD CONSTRAINT asset_register_number_key UNIQUE (asset_id, tick_date, register_number);")


def downgrade():
    op.execute("ALTER TABLE pystock_tick DROP CONSTRAINT asset_register_number_key;")
