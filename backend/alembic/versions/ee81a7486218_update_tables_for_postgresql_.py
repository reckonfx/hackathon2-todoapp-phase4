"""Update tables for PostgreSQL compatibility

Revision ID: ee81a7486218
Revises: 001_initial
Create Date: 2026-01-15 20:11:48.523281

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee81a7486218'
down_revision = '001_initial'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Update tasks table for PostgreSQL compatibility
    # Add the completed_at column if it doesn't exist
    # Note: For SQLite, we'll skip constraint modifications since SQLite doesn't support ALTER for constraints
    from sqlalchemy import inspect

    # Check if we're using SQLite
    engine = op.get_bind()
    inspector = inspect(engine)

    # Get current columns in the tasks table
    columns = [col['name'] for col in inspector.get_columns('tasks')]

    # Add completed_at column if it doesn't exist
    if 'completed_at' not in columns:
        op.add_column('tasks', sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    # Remove the completed_at column if it exists
    from sqlalchemy import inspect

    # Check if we're using SQLite
    engine = op.get_bind()
    inspector = inspect(engine)

    # Get current columns in the tasks table
    columns = [col['name'] for col in inspector.get_columns('tasks')]

    # Drop completed_at column if it exists
    if 'completed_at' in columns:
        op.drop_column('tasks', 'completed_at')