"""email_username_indexes

Revision ID: 6fde4051b860
Revises: c72db41825bd
Create Date: 2018-04-27 18:45:17.729548

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import func
from app.user.models import User



# revision identifiers, used by Alembic.
revision = '6fde4051b860'
down_revision = 'c72db41825bd'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(sa.schema.CreateIndex(sa.Index('ix_user_email', func.lower(User.email))))
    # op.execute(sa.schema.CreateIndex(sa.Index('users_username_index', func.lower(User.username))))
    sa.Index('ix_user_username', func.lower(User.email)).create(bind=op.get_bind())


def downgrade():
    sa.Index('ix_user_username').drop(bind=op.get_bind())
    sa.Index('ix_user_email').drop(bind=op.get_bind())
