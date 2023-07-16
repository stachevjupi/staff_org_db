"""empty message

Revision ID: 0ca18f38df2c
Revises: 1c00b2071bc8
Create Date: 2023-07-16 03:02:48.634107

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ca18f38df2c'
down_revision = '1c00b2071bc8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('chapter',
               existing_type=sa.VARCHAR(length=40),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('chapter',
               existing_type=sa.VARCHAR(length=40),
               nullable=False)

    # ### end Alembic commands ###
