"""add results to quiz completions

Revision ID: 12049328fd0a
Revises: 291331bea272
Create Date: 2024-09-11 10:23:37.753893

"""
from alembic import op
from sqlalchemy.dialects import postgresql
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12049328fd0a'
down_revision = '291331bea272'
branch_labels = None
depends_on = None


def upgrade():
    # Add the 'responses' column
    op.add_column('quiz_completions', sa.Column(
        'responses',
        postgresql.JSONB(astext_type=sa.Text()),
        nullable=False,
        server_default=sa.text("'{}'::jsonb")
    ))


def downgrade():
    # Remove the 'responses' column
    op.drop_column('quiz_completions', 'responses')
