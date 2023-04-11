"""add quiz completions

Revision ID: cd2fe647faf7
Revises: d4d8e2b8e957
Create Date: 2023-04-11 09:02:30.838909

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd2fe647faf7'
down_revision = 'd4d8e2b8e957'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'quiz_completions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('quiz_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('passed', sa.Boolean(), nullable=False),
        sa.Column('submit_ts', sa.TIMESTAMP(), nullable=False),
        sa.ForeignKeyConstraint(['quiz_id'], ['quizzes.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('quiz_completions')
