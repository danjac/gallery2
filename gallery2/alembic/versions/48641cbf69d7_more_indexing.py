"""more indexing

Revision ID: 48641cbf69d7
Revises: 189a3438e287
Create Date: 2014-01-08 12:13:42.491653

"""

# revision identifiers, used by Alembic.
revision = '48641cbf69d7'
down_revision = '189a3438e287'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    op.create_index('ix_users_verification_code', 'users', ['verification_code'], unique=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_users_verification_code', 'users')
    op.drop_index('ix_users_username', 'users')
    op.drop_index('ix_users_email', 'users')
    ### end Alembic commands ###