"""
Refactor: Move name, is_admin, is_recruiter from users to profiles; set profile.id = user.id
"""
from alembic import op
import sqlalchemy as sa

revision = 'refactor_user_profile_split'
down_revision = 'add_can_post_jobs_to_profile'
branch_labels = None
depends_on = None


def upgrade():
    # Add new columns to profiles
    op.add_column('profiles', sa.Column('name', sa.String(length=100)))
    op.add_column('profiles', sa.Column('is_admin', sa.Boolean(),
                  nullable=False, server_default=sa.false()))
    op.add_column('profiles', sa.Column('is_recruiter', sa.Boolean(),
                  nullable=False, server_default=sa.false()))
    # Remove columns from users
    op.drop_column('users', 'name')
    op.drop_column('users', 'is_admin')
    op.drop_column('users', 'is_recruiter')


def downgrade():
    # Add columns back to users
    with op.batch_alter_table('users') as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=100)))
        batch_op.add_column(sa.Column('is_admin', sa.Boolean(),
                            nullable=False, server_default=sa.false()))
        batch_op.add_column(sa.Column('is_recruiter', sa.Boolean(),
                            nullable=False, server_default=sa.false()))
    # Remove columns from profiles
    op.drop_column('profiles', 'name')
    op.drop_column('profiles', 'is_admin')
    op.drop_column('profiles', 'is_recruiter')
