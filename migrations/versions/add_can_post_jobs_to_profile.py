"""
Add can_post_jobs boolean to Profile
"""
import sqlalchemy as sa
from alembic import op
revision = 'add_can_post_jobs_to_profile'
down_revision = 'add_profile_table'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('profiles', sa.Column('can_post_jobs', sa.Boolean(),
                  nullable=False, server_default=sa.false()))


def downgrade():
    op.drop_column('profiles', 'can_post_jobs')
