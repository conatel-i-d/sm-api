"""create results table

Revision ID: 2b60825ec877
Revises: 7e633f4a3f96
Create Date: 2019-11-11 17:58:52.193982

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b60825ec877'
down_revision = '7e633f4a3f96'
branch_labels = None
depends_on = None


def upgrade():
  op.create_table(
        'result',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('job_id', sa.Integer, nullable=False, unique=True),
        sa.Column('type', sa.String(255), nullable=False),
        sa.Column('result', sa.JSON, nullable=False)
    )

def downgrade():
  op.drop_table('switch')
