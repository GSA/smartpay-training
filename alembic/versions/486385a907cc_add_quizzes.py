"""add quizzes

Revision ID: 486385a907cc
Revises: 4a7071546e35
Create Date: 2023-04-04 11:54:08.277897

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '486385a907cc'
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
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'quiz_questions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('text', sa.String(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('quiz_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['quiz_id'], ['quizzes.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'quiz_choices',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('text', sa.String(), nullable=False),
        sa.Column('correct', sa.Boolean(), nullable=False),
        sa.Column('question_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['question_id'], ['quiz_questions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('quiz_choices')
    op.drop_table('quiz_questions')
    op.drop_table('quizzes')
