"""
Refactor: add name to users, drop is_admin/is_recruiter from profiles.
role on profiles is the single source of truth for permissions.
"""
from alembic import op
import sqlalchemy as sa

revision = 'refactor_role_and_name'
down_revision = 'fix_missing_columns'
branch_labels = None
depends_on = None


def upgrade():
    # Add name to users
    op.add_column('users', sa.Column('name', sa.String(length=100), nullable=True))

    # Drop is_admin and is_recruiter from profiles (role is the source of truth)
    op.drop_column('profiles', 'is_admin')
    op.drop_column('profiles', 'is_recruiter')


def downgrade():
    op.add_column('profiles', sa.Column('is_recruiter', sa.Boolean(),
                  nullable=False, server_default=sa.false()))
    op.add_column('profiles', sa.Column('is_admin', sa.Boolean(),
                  nullable=False, server_default=sa.false()))
    op.drop_column('users', 'name')
