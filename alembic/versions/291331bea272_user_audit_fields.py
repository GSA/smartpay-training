"""user-audit-fields

Revision ID: 291331bea272
Revises: a5fbdcd0e719
Create Date: 2024-07-19 09:06:27.754024

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '291331bea272'
down_revision = 'a5fbdcd0e719'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('created_on', sa.DateTime, nullable=False, server_default=sa.func.current_timestamp()))
    op.add_column('users', sa.Column('created_by', sa.String(), nullable=False, server_default='Migrated'))
    op.alter_column('users', 'created_by', server_default=None)
    op.add_column('users', sa.Column('modified_on', sa.DateTime, nullable=True))
    op.add_column('users', sa.Column('modified_by', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'created_on')
    op.drop_column('users', 'created_by')
    op.drop_column('users', 'modified_on')
    op.drop_column('users', 'modified_by')
