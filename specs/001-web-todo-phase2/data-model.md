# Data Model: Phase-2 Web-Based Todo Application

## User Entity

### Fields
- **id**: UUID (Primary Key) - Unique identifier for the user
- **email**: String (Unique, Required) - User's email address for login
- **password_hash**: String (Required) - Securely hashed password
- **name**: String (Optional) - User's display name
- **created_at**: DateTime - Timestamp when user account was created
- **updated_at**: DateTime - Timestamp when user account was last updated
- **is_active**: Boolean - Whether the user account is active (default: true)

### Validation Rules
- Email must be valid email format
- Email must be unique across all users
- Password must meet security requirements (minimum length, complexity)
- Name, if provided, must not exceed 100 characters

## Task Entity

### Fields
- **id**: UUID (Primary Key) - Unique identifier for the task
- **user_id**: UUID (Foreign Key) - Reference to the owning user
- **title**: String (Required) - Brief summary of the task
- **description**: Text (Optional) - Detailed notes about the task
- **completed**: Boolean - Whether the task is completed (default: false)
- **created_at**: DateTime - Timestamp when task was created
- **updated_at**: DateTime - Timestamp when task was last updated

### Validation Rules
- Title must not be empty
- Title must not exceed 200 characters
- Description, if provided, must not exceed 1000 characters
- Task must belong to a valid user
- Only the task owner can modify the task

### Relationships
- **User (1)** ←→ **Task (Many)**: One user can own many tasks
- Foreign key constraint ensures referential integrity

## State Transitions

### Task State Transitions
- **Active** → **Completed**: When user marks task as complete
- **Completed** → **Active**: When user unmarks task as complete

## Data Integrity Constraints

### Database Constraints
- Foreign key constraints to ensure referential integrity
- Unique constraints on user email
- Not-null constraints on required fields
- Check constraints for boolean field validation

### Business Rules
- Users can only access their own tasks
- Tasks cannot be created without a valid user
- Task ownership cannot be changed after creation
- Completed status can only be modified by the task owner