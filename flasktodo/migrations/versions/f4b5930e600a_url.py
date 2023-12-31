"""URL

Revision ID: f4b5930e600a
Revises: b0e73087435b
Create Date: 2023-07-22 13:52:34.594013

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4b5930e600a'
down_revision = 'b0e73087435b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('todo', schema=None) as batch_op:
        batch_op.add_column(sa.Column('url', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=True))
        batch_op.alter_column('todo',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.drop_column('due_date')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('todo', schema=None) as batch_op:
        batch_op.add_column(sa.Column('due_date', sa.DATETIME(), nullable=True))
        batch_op.alter_column('todo',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.drop_column('created_at')
        batch_op.drop_column('url')

    # ### end Alembic commands ###
