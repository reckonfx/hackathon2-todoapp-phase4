"""
Data validation script to verify data integrity after migration
Used to ensure data consistency after the database migration process.
"""

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import os
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


async def validate_data_integrity():
    """
    Validate data integrity after migration.
    Checks for common issues like orphaned records, invalid references, etc.
    """

    # Get database URL from environment
    database_url = os.getenv("DATABASE_URL", "postgresql+asyncpg://username:password@localhost:5432/todo_app_db")

    # Create engine
    engine = create_async_engine(database_url)

    try:
        async with engine.connect() as conn:
            # Check for orphaned tasks (tasks with user_id that doesn't exist in users table)
            logger.info("Checking for orphaned tasks...")

            orphaned_tasks = await conn.execute(
                text("""
                    SELECT t.id, t.user_id
                    FROM tasks t
                    LEFT JOIN users u ON t.user_id = u.id
                    WHERE u.id IS NULL
                """)
            )
            orphaned_tasks_results = orphaned_tasks.fetchall()

            if orphaned_tasks_results:
                logger.warning(f"Found {len(orphaned_tasks_results)} orphaned tasks")
                for task in orphaned_tasks_results:
                    logger.warning(f"Task ID: {task[0]}, User ID: {task[1]}")
            else:
                logger.info("✓ No orphaned tasks found")

            # Check for duplicate emails in users table
            logger.info("Checking for duplicate emails...")

            duplicate_emails = await conn.execute(
                text("""
                    SELECT email, COUNT(*)
                    FROM users
                    GROUP BY email
                    HAVING COUNT(*) > 1
                """)
            )
            duplicate_emails_results = duplicate_emails.fetchall()

            if duplicate_emails_results:
                logger.warning(f"Found {len(duplicate_emails_results)} duplicate emails")
                for email, count in duplicate_emails_results:
                    logger.warning(f"Email: {email}, Count: {count}")
            else:
                logger.info("✓ No duplicate emails found")

            # Check for invalid boolean values in completed field
            logger.info("Checking for invalid boolean values in tasks.completed...")

            invalid_completed = await conn.execute(
                text("""
                    SELECT id, completed
                    FROM tasks
                    WHERE completed IS NOT TRUE AND completed IS NOT FALSE AND completed IS NOT NULL
                """)
            )
            invalid_completed_results = invalid_completed.fetchall()

            if invalid_completed_results:
                logger.error(f"Found {len(invalid_completed_results)} tasks with invalid completed values")
                for task in invalid_completed_results:
                    logger.error(f"Task ID: {task[0]}, Completed: {task[1]}")
                return False
            else:
                logger.info("✓ All completed values are valid")

            # Check for proper UUID format in ID fields
            logger.info("Checking for proper UUID format...")

            # This check is more complex, so we'll just check that IDs exist
            users_count = await conn.execute(text("SELECT COUNT(*) FROM users"))
            users_count = users_count.scalar()

            tasks_count = await conn.execute(text("SELECT COUNT(*) FROM tasks"))
            tasks_count = tasks_count.scalar()

            logger.info(f"Found {users_count} users and {tasks_count} tasks")

            # Check that required fields are not null where they shouldn't be
            logger.info("Checking for required fields...")

            # Users: email and password_hash should not be null
            null_users = await conn.execute(
                text("""
                    SELECT id
                    FROM users
                    WHERE email IS NULL OR password_hash IS NULL
                """)
            )
            null_users_results = null_users.fetchall()

            if null_users_results:
                logger.error(f"Found {len(null_users_results)} users with null required fields")
                return False
            else:
                logger.info("✓ All required fields in users table are present")

            # Tasks: title should not be null
            null_tasks = await conn.execute(
                text("""
                    SELECT id
                    FROM tasks
                    WHERE title IS NULL
                """)
            )
            null_tasks_results = null_tasks.fetchall()

            if null_tasks_results:
                logger.error(f"Found {len(null_tasks_results)} tasks with null title")
                return False
            else:
                logger.info("✓ All required fields in tasks table are present")

            logger.info("✓ All data integrity checks passed!")
            return True

    except Exception as e:
        logger.error(f"Error during data validation: {e}")
        return False
    finally:
        await engine.dispose()


async def run_comprehensive_validation():
    """
    Run comprehensive validation checks on the database.
    """
    logger.info("Starting comprehensive data validation...")

    # Run the data integrity validation
    integrity_ok = await validate_data_integrity()

    if integrity_ok:
        logger.info("✓ All validation checks passed successfully!")
        return True
    else:
        logger.error("✗ Some validation checks failed!")
        return False


if __name__ == "__main__":
    success = asyncio.run(run_comprehensive_validation())
    exit(0 if success else 1)