<%!
from alembic import op
import sqlalchemy as sa
%>
"""empty message

Revision ID: ${up_revision}
Revises: ${down_revision | none}
Create Date: ${create_date}
"""

from alembic import op
import sqlalchemy as sa

revision = '${up_revision}'
down_revision = ${repr(down_revision)}
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
