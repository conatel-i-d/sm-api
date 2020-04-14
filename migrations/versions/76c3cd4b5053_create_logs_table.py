"""create logs table

Revision ID: 76c3cd4b5053
Revises: a2708f0d3454
Create Date: 2019-11-22 11:15:30.644292

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76c3cd4b5053'
down_revision = '2b60825ec877'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'logs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('http_method', sa.String(30), nullable=True),
        sa.Column('http_url', sa.String(30), nullable=True),
        sa.Column('payload', sa.String(1000), nullable=True),
        sa.Column('user_name', sa.String(255), nullable=False),
        sa.Column('user_email', sa.String(255), nullable=True),
        sa.Column('response_status_code', sa.Column(sa.Integer), nullable=True),
        sa.Column('message', sa.String(255), nullable=True),
        sa.Column('date_start', sa.DateTime, nullable=False),
        sa.Column('date_end', sa.DateTime, nullable=False)
    )


def downgrade():
    op.drop_table('logs')
