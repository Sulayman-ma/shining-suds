"""switched to accepted terms boolean instead of is_active

Revision ID: eb67f598900c
Revises: 1e6b612f7adb
Create Date: 2024-01-19 06:44:08.380279

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb67f598900c'
down_revision = '1e6b612f7adb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('accepted_terms', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('accepted_terms')

    # ### end Alembic commands ###