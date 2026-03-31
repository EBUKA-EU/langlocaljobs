"""
Remove can_post_jobs from Profile
"""
from alembic import op
import sqlalchemy as sa

revision = 'rmv_can_post_from_profile'
down_revision = 'refactor_user_profile_split'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('profiles', 'can_post_jobs')


def downgrade():
    op.add_column('profiles', sa.Column('can_post_jobs', sa.Boolean(),
                  nullable=False, server_default=sa.false()))
