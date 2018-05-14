"""revise review start id

Revision ID: ea6a8bac4e76
Revises: f7760f520309
Create Date: 2018-05-14 07:39:10.114302

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea6a8bac4e76'
down_revision = 'f7760f520309'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('ALTER SEQUENCE rev_id_seq RESTART 1000;')


def downgrade():
    op.execute('ALTER SEQUENCE rev_id_seq RESTART 1;')
