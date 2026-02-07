# Data Model: Chat API & Database Contracts

**Feature**: 004-chat-api-db-contracts
**Date**: 2026-01-28
**Status**: Complete

## Overview

This data model extends the Phase II database with two new entities for conversation persistence. The existing `users` and `tasks` tables are reused without modification.

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        PHASE II (FROZEN)                             │
│  ┌─────────────┐         ┌─────────────┐                            │
│  │   users     │ 1───M   │   tasks     │                            │
│  │─────────────│         │─────────────│                            │
│  │ id (PK)     │────────►│ id (PK)     │                            │
│  │ email       │         │ user_id (FK)│                            │
│  │ password_   │         │ title       │                            │
│  │   hash      │         │ description │                            │
│  │ name        │         │ completed   │                            │
│  │ created_at  │         │ created_at  │                            │
│  │ updated_at  │         │ updated_at  │                            │
│  │ is_active   │         └─────────────┘                            │
│  └─────────────┘                                                     │
│         │                                                            │
└─────────┼────────────────────────────────────────────────────────────┘
          │
          │ 1
          │
┌─────────┼────────────────────────────────────────────────────────────┐
│         │              PHASE III (NEW)                               │
│         │ M                                                          │
│  ┌──────▼──────┐         ┌─────────────┐                            │
│  │conversations│ 1───M   │  messages   │                            │
│  │─────────────│         │─────────────│                            │
│  │ id (PK)     │────────►│ id (PK)     │                            │
│  │ user_id (FK)│         │ conversation│                            │
│  │ title       │         │   _id (FK)  │                            │
│  │ created_at  │         │ role        │                            │
│  │ updated_at  │         │ content     │                            │
│  └─────────────┘         │ tool_calls  │                            │
│                          │ created_at  │                            │
│                          └─────────────┘                            │
└─────────────────────────────────────────────────────────────────────┘
```

## Existing Entities (Phase II - Reused)

### User Entity

**Table**: `users`
**Status**: FROZEN - No modifications

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | Login email |
| password_hash | VARCHAR(255) | NOT NULL | Hashed password |
| name | VARCHAR(100) | NULL | Display name |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Account creation |
| updated_at | TIMESTAMP | NOT NULL | Last update |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Account status |

### Task Entity

**Table**: `tasks`
**Status**: FROZEN - No modifications

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| user_id | UUID | FK → users.id, NOT NULL | Task owner |
| title | VARCHAR(200) | NOT NULL | Task title |
| description | TEXT | NULL | Task details |
| completed | BOOLEAN | NOT NULL, DEFAULT FALSE | Completion status |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMP | NOT NULL | Last update |

## New Entities (Phase III)

### Conversation Entity

**Table**: `conversations`
**Purpose**: Track chat sessions between users and the AI assistant
**Spec Reference**: DER-005 to DER-010

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique identifier |
| user_id | UUID | FK → users.id, NOT NULL, ON DELETE CASCADE | Conversation owner |
| title | VARCHAR(100) | NULL | Display title (auto-generated or user-set) |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Session start |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last activity |

**Indexes**:
- `idx_conversations_user_id` on `user_id` (frequent lookup by user)
- `idx_conversations_updated_at` on `updated_at` (recent conversations)

**Validation Rules**:
- title, if provided, must not exceed 100 characters
- user_id must reference a valid, active user
- created_at and updated_at are server-generated only

### Message Entity

**Table**: `messages`
**Purpose**: Store individual messages within conversations
**Spec Reference**: DER-011 to DER-018

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique identifier |
| conversation_id | UUID | FK → conversations.id, NOT NULL, ON DELETE CASCADE | Parent conversation |
| role | VARCHAR(20) | NOT NULL, CHECK (role IN ('user', 'assistant')) | Message sender |
| content | TEXT | NOT NULL, CHECK (length(content) BETWEEN 1 AND 10000) | Message text |
| tool_calls | JSONB | NULL | MCP tool invocations (assistant only) |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Message timestamp |

**Indexes**:
- `idx_messages_conversation_id` on `conversation_id` (load messages for conversation)
- `idx_messages_created_at` on `conversation_id, created_at` (ordering within conversation)

**Validation Rules**:
- content must be 1-10,000 characters
- role must be exactly 'user' or 'assistant'
- tool_calls only allowed when role = 'assistant'
- created_at is server-generated only

**Tool Calls Schema** (JSONB):
```json
[
  {
    "tool": "string",      // Tool name (e.g., "add_task")
    "parameters": {},      // Parameters passed to tool
    "result": {}           // Tool execution result
  }
]
```

## Relationships

### User → Conversations (1:M)
- One user can have many conversations
- Deleting a user cascades to delete all their conversations
- Spec Reference: DER-006, DER-019, DER-022

### Conversation → Messages (1:M)
- One conversation contains many messages
- Deleting a conversation cascades to delete all its messages
- Spec Reference: DER-012, DER-020, DER-021

### User → Tasks (1:M) - Existing
- One user can have many tasks
- This relationship is unchanged from Phase II
- MCP tools access tasks via this relationship

## Data Integrity Constraints

### Foreign Key Constraints

| Constraint | Table | Column | References | On Delete |
|------------|-------|--------|------------|-----------|
| fk_conversations_user | conversations | user_id | users.id | CASCADE |
| fk_messages_conversation | messages | conversation_id | conversations.id | CASCADE |

### Business Rules

1. **No Orphan Prevention** (DER-021, DER-022):
   - Messages cannot exist without a valid conversation
   - Conversations cannot exist without a valid user
   - Enforced via NOT NULL + FK constraints

2. **Timestamp Server-Generation** (DER-023):
   - created_at defaults to NOW()
   - updated_at managed by trigger or application
   - Client cannot override timestamps

3. **Message Ordering** (DER-018):
   - Messages ordered by created_at within conversation
   - Composite index ensures efficient ordering

## State Transitions

### Conversation States

```
                 ┌──────────────┐
      create     │              │  update (new message)
    ──────────►  │   ACTIVE     │ ◄─────────────────┐
                 │              │                    │
                 └──────┬───────┘                    │
                        │                            │
                   delete                            │
                        │                            │
                        ▼                            │
                 ┌──────────────┐                    │
                 │   DELETED    │                    │
                 │  (cascade)   │                    │
                 └──────────────┘                    │
```

### Message Lifecycle

```
1. User sends message to API
2. API creates Message(role='user') immediately
3. Agent processes message
4. API creates Message(role='assistant') with response
5. Both messages linked to same conversation
```

## Migration Strategy

### Migration Order

1. Create `conversations` table (depends on `users`)
2. Create `messages` table (depends on `conversations`)
3. Create indexes
4. No data migration needed (new tables start empty)

### Rollback Strategy

1. Drop `messages` table first (no dependents)
2. Drop `conversations` table
3. No impact on existing Phase II data

## SQLModel Definitions

### Conversation Model

```python
class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )
    user_id: uuid.UUID = Field(
        foreign_key="users.id",
        nullable=False,
        index=True
    )
    title: str | None = Field(
        default=None,
        max_length=100
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )

    # Relationships
    messages: list["Message"] = Relationship(back_populates="conversation")
```

### Message Model

```python
class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )
    conversation_id: uuid.UUID = Field(
        foreign_key="conversations.id",
        nullable=False,
        index=True
    )
    role: str = Field(
        nullable=False,
        sa_column=Column(String(20), CheckConstraint("role IN ('user', 'assistant')"))
    )
    content: str = Field(
        nullable=False,
        sa_column=Column(Text, CheckConstraint("length(content) BETWEEN 1 AND 10000"))
    )
    tool_calls: dict | None = Field(
        default=None,
        sa_column=Column(JSONB)
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )

    # Relationships
    conversation: Conversation = Relationship(back_populates="messages")
```
