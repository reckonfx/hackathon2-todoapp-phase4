# Data Model: Backend Stability for Phase-2 Web Todo Application

## Overview

This document defines the data models and entities used in the Phase-2 Web Todo application backend, with focus on authentication and user management systems that need stability fixes.

## Entity Models

### 1. User Entity

**Entity Name**: User
**Table**: users

#### Fields:
- `id`: UUID (Primary Key, auto-generated)
  - Type: UUID (as_uuid=True)
  - Constraints: Primary key, not null, auto-generated
  - Validation: Must be valid UUID format

- `email`: String
  - Type: String
  - Constraints: Unique, not null, indexed
  - Validation: Must be valid email format
  - Length: Maximum 255 characters

- `password_hash`: String
  - Type: String
  - Constraints: Not null
  - Validation: Must be valid bcrypt hash format
  - Length: Variable (typically 60+ characters for bcrypt)

- `name`: String (Optional)
  - Type: String
  - Constraints: Nullable
  - Validation: Alphanumeric with spaces, 1-100 characters
  - Length: Maximum 100 characters

- `created_at`: DateTime
  - Type: DateTime (with timezone)
  - Constraints: Auto-generated server timestamp
  - Format: ISO 8601

- `updated_at`: DateTime (Optional)
  - Type: DateTime (with timezone)
  - Constraints: Auto-updated server timestamp
  - Format: ISO 8601

- `is_active`: Boolean
  - Type: Boolean
  - Constraints: Not null, default true
  - Values: true/false

#### Relationships:
- One User to Many Tasks (via foreign key in tasks table)

#### Validation Rules:
- Email must be unique across all users
- Password hash must be valid bcrypt format
- Email must follow RFC 5322 standard
- User must be active (is_active = true) for authentication

#### State Transitions:
- User starts as active upon registration
- User can be deactivated (is_active = false) by admin
- User deletion is soft-delete (mark as inactive)

### 2. Task Entity

**Entity Name**: Task
**Table**: tasks

#### Fields:
- `id`: UUID (Primary Key, auto-generated)
  - Type: UUID (as_uuid=True)
  - Constraints: Primary key, not null, auto-generated

- `user_id`: UUID (Foreign Key)
  - Type: UUID (as_uuid=True)
  - Constraints: Foreign key to users.id, not null
  - Relationship: Belongs to one User

- `title`: String
  - Type: String
  - Constraints: Not null
  - Validation: 1-255 characters

- `description`: String (Optional)
  - Type: String
  - Constraints: Nullable
  - Validation: Up to 1000 characters

- `completed`: Boolean
  - Type: Boolean
  - Constraints: Not null, default false
  - Values: true/false

- `created_at`: DateTime
  - Type: DateTime (with timezone)
  - Constraints: Auto-generated server timestamp
  - Format: ISO 8601

- `updated_at`: DateTime (Optional)
  - Type: DateTime (with timezone)
  - Constraints: Auto-updated server timestamp
  - Format: ISO 8601

#### Relationships:
- Many Tasks to One User (via user_id foreign key)

#### Validation Rules:
- Task must belong to an active user
- Title must not be empty
- Task can only be modified by the owner user

### 3. Authentication Token

**Entity Name**: Authentication Token (Transient)
**Storage**: JWT Token (Client-side storage)

#### Fields:
- `access_token`: String
  - Type: String (JWT)
  - Format: Base64 encoded JWT with header.payload.signature
  - Validation: Must be valid JWT format

- `token_type`: String
  - Type: String
  - Values: "bearer" (fixed value)

- `expires_at`: DateTime
  - Type: DateTime
  - Format: ISO 8601
  - Validation: Future timestamp

#### Validation Rules:
- Token must be properly signed with server secret
- Token must not be expired at time of validation
- Token must contain valid user identifier (email/ID)

## Schema Definitions

### 1. User Schemas (Validation Only)

#### UserBase
- `email`: EmailStr (Required)
- `name`: Optional[str] (Max 100 chars)

#### UserCreate
- Inherits from UserBase
- `password`: str (Min 1 char, max 72 bytes before hashing)

#### UserRegister
- Inherits from UserCreate

#### UserLogin
- `email`: EmailStr (Required)
- `password`: str (Min 1 char, max 72 bytes)

#### UserPublic
- `id`: UUID (Required)
- Inherits from UserBase (without password)

#### UserInDB
- `id`: UUID (Required)
- `is_active`: bool (Default: True)
- `created_at`: datetime
- Inherits from UserBase

### 2. Authentication Schemas

#### Token
- `access_token`: str (JWT format)
- `token_type`: str ("bearer")

#### TokenData
- `username`: Optional[str]

## Database Constraints

### 1. Primary Keys
- All entities use UUID primary keys for global uniqueness
- Auto-generated using uuid.uuid4()

### 2. Foreign Keys
- Task.user_id references User.id
- Enforced with database-level constraints

### 3. Uniqueness
- User.email must be unique
- Enforced with database-level unique constraint and index

### 4. Indexes
- User.email: Unique index for fast lookup
- User.id: Primary key index
- Task.user_id: Foreign key index for relationship queries

## Data Validation Rules

### 1. Password Handling
- Raw password maximum: 72 bytes (before hashing)
- Password hashing: Single bcrypt operation with proper salt
- No double hashing allowed in any part of the system
- Schema layer does not perform any password transformation

### 2. Email Validation
- Must conform to RFC 5322 email standards
- Length maximum: 255 characters
- Case-insensitive comparison for uniqueness

### 3. Timestamp Handling
- All datetime fields use timezone-aware storage
- Created timestamps set automatically on insert
- Updated timestamps set automatically on update

## Security Considerations

### 1. Password Security
- Passwords stored only as bcrypt hashes
- No plaintext passwords stored in database
- Hashing performed only in service layer
- Schema layer performs only validation

### 2. Session Management
- JWT tokens contain minimal required information
- Tokens have configurable expiration times
- Token validation happens server-side

### 3. Data Integrity
- Foreign key constraints enforce referential integrity
- Unique constraints prevent duplicate accounts
- All database operations use parameterized queries to prevent injection