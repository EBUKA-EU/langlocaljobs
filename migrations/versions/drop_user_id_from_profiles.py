"""
Drop user_id column from profiles and set id as PK/FK to users.id
"""
from alembic import op
import sqlalchemy as sa

revision = 'drop_user_id_from_profiles'
down_revision = 'remove_can_post_jobs_from_profile'
branch_labels = None
depends_on = None


def upgrade():
    # Use batch mode for all changes (SQLite safe)
    with op.batch_alter_table('profiles') as batch_op:
        batch_op.drop_column('user_id')
        # Drop any existing FK on id (if present)
        # Recreate FK on id to users.id
        # Create FK on id to users.id (if not already present)
        batch_op.create_foreign_key('fk_profiles_id_users', 'users', ['id'], ['id'])


def downgrade():
    # Add user_id column back and remove FK on id
    with op.batch_alter_table('profiles') as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(),
                            sa.ForeignKey('users.id'), unique=True, nullable=False))
        # No need to drop constraint if it doesn't exist
