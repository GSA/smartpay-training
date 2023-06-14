"""Add Roles Table

Revision ID: 2faf32f24621
Revises: 46480965d1de
Create Date: 2023-06-06 17:17:01.050091

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2faf32f24621'
down_revision = '46480965d1de'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'roles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_roles_name'), 'roles', ['name'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_roles_name'), table_name='roles')
    op.drop_table('roles')
