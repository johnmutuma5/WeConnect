"""add business name index

Revision ID: 2ad03df3591d
Revises: 6fde4051b860
Create Date: 2018-05-07 06:00:14.592333

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import func
from app.business.models import Business


# revision identifiers, used by Alembic.
revision = '2ad03df3591d'
down_revision = '6fde4051b860'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'users', ['email'])
    sa.Index('ix_business_name', func.LOWER(Business.name)).create(bind=op.get_bind())
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    sa.Index('ix_business_name', func.LOWER(Business.name)).drop(bind=op.get_bind())
    # ### end Alembic commands ###