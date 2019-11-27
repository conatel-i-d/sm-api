"""create logs table

Revision ID: 76c3cd4b5053
Revises: a2708f0d3454
Create Date: 2019-11-22 11:15:30.644292

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76c3cd4b5053'
down_revision = 'a2708f0d3454'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'logs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('event_type', sa.String(30), nullable=False),
        sa.Column('event_result', sa.String(30), nullable=False),
        sa.Column('entity', sa.String(30), nullable=False),
        sa.Column('payload', sa.String(500), nullable=True),
        sa.Column('user_id', sa.String(255), nullable=False),
        sa.Column('date', sa.DateTime, nullable=False)
    )


def downgrade():
    op.drop_table('logs')
