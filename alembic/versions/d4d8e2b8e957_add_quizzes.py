"""add quizzes

Revision ID: d4d8e2b8e957
Revises: 4a7071546e35
Create Date: 2023-04-06 15:52:24.848458

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd4d8e2b8e957'
down_revision = '4a7071546e35'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'quizzes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('topic', sa.String(), nullable=False),
        sa.Column('audience', sa.String(), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=False),
        sa.Column('content', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('quizzes')
