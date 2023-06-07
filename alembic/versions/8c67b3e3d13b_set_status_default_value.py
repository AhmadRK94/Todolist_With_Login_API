"""set status default value

Revision ID: 8c67b3e3d13b
Revises: 97e8f58795d2
Create Date: 2023-06-07 18:54:36.347092

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8c67b3e3d13b"
down_revision = "97e8f58795d2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(table_name="todos", column_name="status", server_default=False)


def downgrade() -> None:
    op.alter_column(table_name="todos", column_name="status", server_default=None)
