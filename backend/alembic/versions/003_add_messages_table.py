"""Add messages table for Phase III chat

Revision ID: 003_add_messages
Revises: 002_add_conversations
Create Date: 2026-01-28 12:01:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '003_add_messages'
down_revision = '002_add_conversations'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create messages table
    # Spec Reference: DER-011 to DER-018
    op.create_table('messages',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()')),
        sa.Column('conversation_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('role', sa.String(20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('tool_calls', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE', name='fk_messages_conversation'),
        # Check constraint for role values (DER-014)
        sa.CheckConstraint("role IN ('user', 'assistant')", name='ck_messages_role'),
        # Check constraint for content length (DER-016)
        sa.CheckConstraint("length(content) BETWEEN 1 AND 10000", name='ck_messages_content_length')
    )

    # Create indexes for efficient queries
    # idx_messages_conversation_id - load messages for conversation
    op.create_index('idx_messages_conversation_id', 'messages', ['conversation_id'], unique=False)
    # idx_messages_created_at - ordering within conversation (composite index)
    op.create_index('idx_messages_conversation_created_at', 'messages', ['conversation_id', 'created_at'], unique=False)


def downgrade() -> None:
    op.drop_index('idx_messages_conversation_created_at', table_name='messages')
    op.drop_index('idx_messages_conversation_id', table_name='messages')
    op.drop_table('messages')
