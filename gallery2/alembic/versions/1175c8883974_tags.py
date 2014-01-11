"""tags

Revision ID: 1175c8883974
Revises: 3b387b077506
Create Date: 2014-01-11 11:06:43.412100

"""

# revision identifiers, used by Alembic.
revision = '1175c8883974'
down_revision = '3b387b077506'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tagged_images', 'image_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('tagged_images', 'tag_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tagged_images', 'tag_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('tagged_images', 'image_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    ### end Alembic commands ###
