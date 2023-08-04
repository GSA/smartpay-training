"""Add report_users_x_agencies table

Revision ID: 3acf0ea1ba59
Revises: 3c4dff3e3e33
Create Date: 2023-06-06 19:35:13.290019

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3acf0ea1ba59'
down_revision = '3c4dff3e3e33'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'report_users_x_agencies',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('agency_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['agency_id'], ['agencies.id'], ),
        sa.PrimaryKeyConstraint('user_id', 'agency_id')
    )


def downgrade() -> None:
    op.drop_table('report_users_x_agencies')
