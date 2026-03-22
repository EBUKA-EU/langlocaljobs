"""
Add Profile table linked to User
"""
import sqlalchemy as sa
from alembic import op
revision = 'add_profile_table'
down_revision = '479600a2661d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'profiles',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey(
            'users.id'), unique=True, nullable=False),
        sa.Column('role', sa.String(length=50),
                  nullable=False, server_default='job_seeker'),
    )


def downgrade():
    op.drop_table('profiles')
