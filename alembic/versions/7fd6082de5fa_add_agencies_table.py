"""add agencies table

Revision ID: 7fd6082de5fa
Revises:
Create Date: 2023-03-16 16:51:51.977844

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7fd6082de5fa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'agencies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_agencies_name'), 'agencies', ['name'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_agencies_name'), table_name='agencies')
    op.drop_table('agencies')
