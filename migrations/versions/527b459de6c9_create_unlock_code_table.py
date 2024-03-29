"""create unlock_code table

Revision ID: 527b459de6c9
Revises: 8ca8454bb12c
Create Date: 2023-05-29 20:06:37.459426

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '527b459de6c9'
down_revision = '8ca8454bb12c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('unlock_code',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ucode_name', sa.String(length=64), nullable=False),
    sa.Column('ucode_create_date', sa.DateTime(), nullable=True),
    sa.Column('ucode_valid_date', sa.DateTime(), nullable=True),
    sa.Column('booking_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['booking_id'], ['booking_order.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('unlock_code', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_unlock_code_ucode_create_date'), ['ucode_create_date'], unique=False)
        batch_op.create_index(batch_op.f('ix_unlock_code_ucode_name'), ['ucode_name'], unique=False)
        batch_op.create_index(batch_op.f('ix_unlock_code_ucode_valid_date'), ['ucode_valid_date'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('unlock_code', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_unlock_code_ucode_valid_date'))
        batch_op.drop_index(batch_op.f('ix_unlock_code_ucode_name'))
        batch_op.drop_index(batch_op.f('ix_unlock_code_ucode_create_date'))

    op.drop_table('unlock_code')
    # ### end Alembic commands ###
