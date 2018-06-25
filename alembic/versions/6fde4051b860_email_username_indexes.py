"""email_username_indexes

Revision ID: 6fde4051b860
Revises: c72db41825bd
Create Date: 2018-04-27 18:45:17.729548

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text



# revision identifiers, used by Alembic.
revision = '6fde4051b860'
down_revision = 'c72db41825bd'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index('ix_user_email', 'users', [text('LOWER(email)')], unique=True)
    op.create_index('ix_user_username', 'users', [text('LOWER(username)')], unique=True)


def downgrade():
    op.drop_index('ix_user_username')
    op.drop_index('ix_user_email')
