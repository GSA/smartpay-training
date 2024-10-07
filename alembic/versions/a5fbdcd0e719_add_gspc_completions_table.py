"""add gspc_completions table

Revision ID: a5fbdcd0e719
Revises: 51b251b1ec2a
Create Date: 2024-05-08 10:43:09.569708

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'a5fbdcd0e719'
down_revision = '51b251b1ec2a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'gspc_completions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('passed', sa.Boolean(), nullable=False),
        sa.Column('certification_expiration_date', sa.Date, nullable=False),
        sa.Column('submit_ts', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('responses', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('gspc_completions')
