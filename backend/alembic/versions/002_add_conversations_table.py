"""Add conversations table for Phase III chat

Revision ID: 002_add_conversations
Revises: ee81a7486218
Create Date: 2026-01-28 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002_add_conversations'
down_revision = 'ee81a7486218'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create conversations table
    # Spec Reference: DER-005 to DER-010
    op.create_table('conversations',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='fk_conversations_user')
    )

    # Create indexes for efficient queries
    # idx_conversations_user_id - frequent lookup by user
    op.create_index('idx_conversations_user_id', 'conversations', ['user_id'], unique=False)
    # idx_conversations_updated_at - recent conversations ordering
    op.create_index('idx_conversations_updated_at', 'conversations', ['updated_at'], unique=False)


def downgrade() -> None:
    op.drop_index('idx_conversations_updated_at', table_name='conversations')
    op.drop_index('idx_conversations_user_id', table_name='conversations')
    op.drop_table('conversations')
