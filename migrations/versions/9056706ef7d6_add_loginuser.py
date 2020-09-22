"""add loginuser

Revision ID: 9056706ef7d6
Revises: 23825ddf6542
Create Date: 2020-09-22 02:45:02.473826

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9056706ef7d6'
down_revision = '23825ddf6542'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('login_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('token', sa.String(length=32), nullable=True),
    sa.Column('token_expiration', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_login_user_token'), 'login_user', ['token'], unique=True)
    op.create_index(op.f('ix_login_user_username'), 'login_user', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_login_user_username'), table_name='login_user')
    op.drop_index(op.f('ix_login_user_token'), table_name='login_user')
    op.drop_table('login_user')
    # ### end Alembic commands ###
