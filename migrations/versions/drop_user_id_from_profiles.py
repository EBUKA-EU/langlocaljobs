"""
Drop user_id column from profiles and set id as PK/FK to users.id
"""
from alembic import op
import sqlalchemy as sa

revision = 'drop_user_id_from_profiles'
down_revision = 'rmv_can_post_from_profile'
branch_labels = None
depends_on = None


def upgrade():
    # Drop user_id column directly (PostgreSQL supports this natively)
    op.drop_column('profiles', 'user_id')
    # Create FK on id to users.id
    op.create_foreign_key('fk_profiles_id_users', 'profiles', 'users', ['id'], ['id'])


def downgrade():
    # Add user_id column back and remove FK on id
    with op.batch_alter_table('profiles') as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(),
                            sa.ForeignKey('users.id'), unique=True, nullable=False))
        # No need to drop constraint if it doesn't exist
