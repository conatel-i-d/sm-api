"""switch

Revision ID: 7e633f4a3f96
Revises: 44ce70d8983e
Create Date: 2019-10-25 15:45:26.106566

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e633f4a3f96'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'switch',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('ip', sa.String(15), nullable=False),
        sa.Column('description', sa.String(255), nullable=True),
        sa.Column('model', sa.String(255), nullable=True),
        sa.Column('ansible_user', sa.String(255), nullable=True),
        sa.Column('ansible_ssh_pass', sa.String(255), nullable=True),
        sa.Column('ansible_ssh_port', sa.Integer, nullable=True),
    )


def downgrade():
    op.drop_table('switch')
