"""add gspc invite table

Revision ID: 51b251b1ec2a
Revises: 3acf0ea1ba59
Create Date: 2024-02-27 13:41:26.028121

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '51b251b1ec2a'
down_revision = '3acf0ea1ba59'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'gspc_invite',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('created_date', sa.DateTime, nullable=False, server_default=sa.func.current_timestamp()),
        sa.Column('certification_expiration_date', sa.Date, nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('gspc_invite')
