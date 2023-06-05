"""Update Agencies Bureau info (DML)

Revision ID: 4bea49807753
Revises: 46480965d1de
Create Date: 2023-06-05 13:34:05.413670

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '4bea49807753'
down_revision = '46480965d1de'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### update agency Department of Agriculture to U.S. Department of Agriculture ###
    op.execute("""
               update agencies
                set name = 'U.S. Department of Agriculture'
                where name ='Department of Agriculture'
               """)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### Roll back to previous version ###
    op.execute("""
               update agencies
                set name = 'Department of Agriculture'
                where name ='U.S. Department of Agriculture'
               """)
    # ### end Alembic commands ###
