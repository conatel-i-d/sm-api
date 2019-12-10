"""update jobs table

Revision ID: a2708f0d3454
Revises: 2b60825ec877
Create Date: 2019-11-22 11:08:31.810728

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2708f0d3454'
down_revision = '2b60825ec877'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('jobs',sa.Column('user_id', sa.String(255), nullable=False, unique=True))


def downgrade():
    op.drop_column('jobs', 'user_id')
