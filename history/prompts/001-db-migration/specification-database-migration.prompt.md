---
id: phr-001-db-migration-spec-20260115
title: Database Migration Specification Creation
stage: spec
created: 2026-01-15
tags: [database, postgresql, neon, migration, sqlite, backend]
---

# Database Migration Specification Creation

## Original Prompt

You are sp.specify, a strict specification-driven system.

PROJECT CONTEXT
---------------
Project Name: Phase-2 Web-Based Todo Application
Frontend: Next.js
Backend: FastAPI (async)
ORM: SQLAlchemy (async)
Current DB: SQLite (sqlite:///./todo_app_local.db)
Target DB: Neon (PostgreSQL)
Migration Tool: Alembic
Environment: Local + Production ready

OBJECTIVE
---------
Migrate the backend database layer from SQLite to Neon PostgreSQL.
Ensure all database operations (create, read, update, delete, merge, migrations)
work correctly and are fully tested.

You MUST produce a step-by-step specification.
Each step MUST clearly state:
1. Which file is modified or created
2. What exact change is required
3. Why the change is needed
4. How to verify the step (test or command)

DO NOT skip steps.
DO NOT assume defaults.
DO NOT mix SQLite logic with PostgreSQL logic.

--------------------------------------------------
STEP 1: ENVIRONMENT VARIABLES
--------------------------------------------------
Specify:
- Which `.env` files must exist
- Which variables must be added or replaced

Required variables:
- DATABASE_URL (PostgreSQL + asyncpg)
- ENV (local / production)
- NEON_POOL_SIZE (optional)

Explicitly state:
- Old SQLite value
- New Neon value format
- Example Neon connection string

--------------------------------------------------
STEP 2: DATABASE CONNECTION LAYER
--------------------------------------------------
File: `app/database/connection.py`

Specify:
- Removal of SQLite engine logic
- Use of `create_async_engine`
- AsyncSession configuration
- Connection pooling settings
- Safe production defaults

Clearly state:
- What code must be deleted
- What code must replace it

--------------------------------------------------
STEP 3: DEPENDENCY INJECTION
--------------------------------------------------
File: `app/database/deps.py` (or equivalent)

Specify:
- Async DB session dependency
- Correct session lifecycle handling
- Error-safe session closing

--------------------------------------------------
STEP 4: MODEL COMPATIBILITY (POSTGRES-SAFE)
--------------------------------------------------
Files: `app/models/*.py`

For each model:
- Identify SQLite-only patterns
- Replace with PostgreSQL-safe types

Explicitly cover:
- DateTime with timezone
- Boolean fields
- String length enforcement
- JSON usage (if any)
- Primary keys and indexes

--------------------------------------------------
STEP 5: ALEMBIC SETUP
--------------------------------------------------
Specify:
- Required folders and files
- `alembic.ini` updates
- `env.py` target_metadata binding

Commands:
- Initialize Alembic
- Generate migration
- Apply migration to Neon

--------------------------------------------------
STEP 6: TABLE CREATION IN NEON
--------------------------------------------------
Define:
- How tables are created ONLY via Alembic
- Why `Base.metadata.create_all()` must not be used
- How to verify tables exist in Neon

--------------------------------------------------
STEP 7: DATA MIGRATION (OPTIONAL)
--------------------------------------------------
Provide two paths:
A) Fresh database (no data)
B) SQLite → Neon migration

Specify:
- Script location
- One-time execution rule
- Validation steps

--------------------------------------------------
STEP 8: CRUD + MERGE OPERATIONS
--------------------------------------------------
Files: `app/repositories/*.py` or `app/services/*.py`

Specify:
- Async CRUD patterns
- Merge / upsert behavior (Postgres-safe)
- Transaction handling
- Rollback strategy

--------------------------------------------------
STEP 9: TESTING REQUIREMENTS
--------------------------------------------------
Define mandatory tests for:
- DB connection
- Table creation
- CRUD operations
- Migration success

Specify:
- pytest structure
- Test database isolation
- Environment separation

--------------------------------------------------
STEP 10: FRONTEND SAFETY CHECK
--------------------------------------------------
File: `frontend/.env.local`

Specify:
- No direct DB exposure
- API base URL only
- Verification checklist

--------------------------------------------------
CONSTRAINTS
-----------
- PostgreSQL only (no SQLite fallback)
- Async SQLAlchemy only
- Alembic required
- Production-safe defaults
- Clear verification after each step

OUTPUT FORMAT
-------------
For EACH step, output:
- Step title
- Files involved
- Code changes (high-level, not verbose)
- Command(s) to run
- Expected result

END SPECIFICATION

## Response Summary

Created a comprehensive specification for migrating the backend database from SQLite to Neon PostgreSQL. The specification includes:

- User scenarios covering the core functionality, migration process, and production configuration
- Functional requirements defining the technical capabilities needed
- Success criteria with measurable outcomes
- Proper validation checklist confirming specification quality

The specification is ready for the planning phase and follows the required format without implementation-specific details that would compromise the technology-agnostic nature of the requirements.

## Key Artifacts Created

- `specs/001-db-migration/spec.md` - Main specification document
- `specs/001-db-migration/checklists/requirements.md` - Validation checklist