"""add pass secure and email columns

Revision ID: c9600ba53a5f
Revises: 74b6ad58f771
Create Date: 2022-05-15 05:44:23.050025

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9600ba53a5f'
down_revision = '74b6ad58f771'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('pass_secure', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('email', sa.String(), nullable=True))
    op.create_unique_constraint(None, 'users', ['email'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'email')
    op.drop_column('users', 'pass_secure')
    # ### end Alembic commands ###
