"""Add bureau column to agencies table

Revision ID: 46480965d1de
Revises: cd2fe647faf7
Create Date: 2023-05-31 16:25:05.338022

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46480965d1de'
down_revision = 'cd2fe647faf7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('agencies', sa.Column('bureau', sa.String(), nullable=True))
    op.execute("""
               ALTER TABLE agencies
               DROP CONSTRAINT IF EXISTS ix_agencies_name;
               """)
    op.execute("""
               DROP INDEX IF EXISTS ix_agencies_name;
               """)
    op.create_index(op.f('ix_agencies_name_bureau'), 'agencies', ['name', 'bureau'], unique=True)


def downgrade() -> None:
    op.drop_index("ix_agencies_name_bureau")
    op.execute("""
               delete from agencies
               where bureau is not null
               """)
    op.drop_column('agencies', 'bureau')
    op.create_index(op.f('ix_agencies_name'), 'agencies', ['name'], unique=True)
