"""added clothes_count to order

Revision ID: c380fd2d2099
Revises: c53ad0656460
Create Date: 2023-11-19 05:52:47.149700

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c380fd2d2099'
down_revision = 'c53ad0656460'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('clothes_count', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.drop_column('clothes_count')

    # ### end Alembic commands ###
