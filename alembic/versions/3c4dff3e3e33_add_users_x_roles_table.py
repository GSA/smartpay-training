"""Add users_x_roles table

Revision ID: 3c4dff3e3e33
Revises: 2faf32f24621
Create Date: 2023-06-06 17:53:18.376421

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c4dff3e3e33'
down_revision = '2faf32f24621'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users_x_roles',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
        sa.PrimaryKeyConstraint('user_id', 'role_id')
    )


def downgrade() -> None:
    op.drop_table('users_x_roles')
