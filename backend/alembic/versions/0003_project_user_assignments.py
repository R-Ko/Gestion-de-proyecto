"""project user assignments

Revision ID: 0003_project_user_assignments
Revises: 0002_add_password_hash_to_users
Create Date: 2026-05-15 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

revision = '0003_project_user_assignments'
down_revision = '0002_add_password_hash_to_users'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user_projects',
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id'), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), primary_key=True),
    )


def downgrade():
    op.drop_table('user_projects')
