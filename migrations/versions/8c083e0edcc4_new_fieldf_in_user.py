"""new fieldf in user

Revision ID: 8c083e0edcc4
Revises: 81f94713127d
Create Date: 2020-08-28 09:47:58.391228

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c083e0edcc4'
down_revision = '81f94713127d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('about_me', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('last_seen', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'last_seen')
    op.drop_column('users', 'about_me')
    # ### end Alembic commands ###
