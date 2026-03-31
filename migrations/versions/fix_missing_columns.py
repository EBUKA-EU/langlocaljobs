"""
Add missing columns: users.last_logged_in, profiles.created_at, profiles.updated_at
Fix role default from job_seeker to user
"""
from alembic import op
import sqlalchemy as sa

revision = 'fix_missing_columns'
down_revision = 'drop_user_id_from_profiles'
branch_labels = None
depends_on = None


def upgrade():
    # Add last_logged_in to users
    op.add_column('users', sa.Column('last_logged_in',
                  sa.DateTime(), nullable=True))

    # Add created_at and updated_at to profiles
    op.add_column('profiles', sa.Column('created_at',
                  sa.DateTime(), nullable=True))
    op.add_column('profiles', sa.Column('updated_at',
                  sa.DateTime(), nullable=True))

    # Fix role default from 'job_seeker' to 'user'
    op.alter_column('profiles', 'role',
                    existing_type=sa.String(length=50),
                    server_default='user',
                    existing_nullable=False)


def downgrade():
    op.drop_column('users', 'last_logged_in')
    op.drop_column('profiles', 'created_at')
    op.drop_column('profiles', 'updated_at')
    op.alter_column('profiles', 'role',
                    existing_type=sa.String(length=50),
                    server_default='job_seeker',
                    existing_nullable=False)
