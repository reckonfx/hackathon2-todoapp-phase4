"""
Data migration script to transfer data from SQLite to PostgreSQL
Used for migrating existing data during the database migration process.
"""

import asyncio
import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def migrate_data_sqlite_to_postgresql():
    """
    Migrate data from SQLite to PostgreSQL database.
    This function handles the transfer of existing data from SQLite to PostgreSQL.
    """

    # Get database URLs from environment
    sqlite_url = os.getenv("DATABASE_URL", "sqlite:///./todo_app_local.db")
    pg_url = os.getenv("POSTGRESQL_MIGRATION_URL", "postgresql+asyncpg://username:password@localhost:5432/todo_app_db")

    print(f"Starting migration from {sqlite_url} to {pg_url}")

    # Create engines for both databases
    sqlite_engine = create_async_engine(sqlite_url)
    pg_engine = create_async_engine(pg_url)

    # Create session makers
    SQLiteSession = sessionmaker(bind=sqlite_engine, class_=AsyncSession, expire_on_commit=False)
    PGSession = sessionmaker(bind=pg_engine, class_=AsyncSession, expire_on_commit=False)

    try:
        # Connect to both databases
        async with SQLiteSession() as sqlite_session:
            async with PGSession() as pg_session:

                # Migrate users first (since tasks depend on users)
                print("Migrating users...")
                users_result = await sqlite_session.execute(text("SELECT * FROM users"))
                users = users_result.fetchall()

                for user_row in users:
                    # Insert user into PostgreSQL
                    await pg_session.execute(
                        text("""
                            INSERT INTO users (id, email, password_hash, name, created_at, updated_at, is_active)
                            VALUES (:id, :email, :password_hash, :name, :created_at, :updated_at, :is_active)
                            ON CONFLICT (email) DO NOTHING
                        """),
                        {
                            'id': str(user_row[0]),  # Convert UUID to string
                            'email': user_row[1],
                            'password_hash': user_row[2],
                            'name': user_row[3],
                            'created_at': user_row[4],
                            'updated_at': user_row[5],
                            'is_active': user_row[6]
                        }
                    )

                # Migrate tasks
                print("Migrating tasks...")
                tasks_result = await sqlite_session.execute(text("SELECT * FROM tasks"))
                tasks = tasks_result.fetchall()

                for task_row in tasks:
                    # Insert task into PostgreSQL
                    await pg_session.execute(
                        text("""
                            INSERT INTO tasks (id, user_id, title, description, completed, completed_at, created_at, updated_at)
                            VALUES (:id, :user_id, :title, :description, :completed, :completed_at, :created_at, :updated_at)
                            ON CONFLICT (id) DO NOTHING
                        """),
                        {
                            'id': str(task_row[0]),
                            'user_id': str(task_row[1]),
                            'title': task_row[2],
                            'description': task_row[3],
                            'completed': task_row[4],
                            'completed_at': task_row[5],
                            'created_at': task_row[6],
                            'updated_at': task_row[7]
                        }
                    )

                # Commit the transaction
                await pg_session.commit()
                print("Migration completed successfully!")

    except Exception as e:
        print(f"Error during migration: {e}")
        raise
    finally:
        await sqlite_engine.dispose()
        await pg_engine.dispose()


async def validate_data_migration():
    """
    Validate that data was correctly migrated from SQLite to PostgreSQL.
    """
    print("Validating data migration...")

    # Get database URLs from environment
    sqlite_url = os.getenv("DATABASE_URL", "sqlite:///./todo_app_local.db")
    pg_url = os.getenv("POSTGRESQL_MIGRATION_URL", "postgresql+asyncpg://username:password@localhost:5432/todo_app_db")

    # Create engines for both databases
    sqlite_engine = create_async_engine(sqlite_url)
    pg_engine = create_async_engine(pg_url)

    try:
        # Count records in both databases
        async with sqlite_engine.connect() as sqlite_conn:
            sqlite_users_count = await sqlite_conn.execute(text("SELECT COUNT(*) FROM users"))
            sqlite_users_count = sqlite_users_count.scalar()

            sqlite_tasks_count = await sqlite_conn.execute(text("SELECT COUNT(*) FROM tasks"))
            sqlite_tasks_count = sqlite_tasks_count.scalar()

        async with pg_engine.connect() as pg_conn:
            pg_users_count = await pg_conn.execute(text("SELECT COUNT(*) FROM users"))
            pg_users_count = pg_users_count.scalar()

            pg_tasks_count = await pg_conn.execute(text("SELECT COUNT(*) FROM tasks"))
            pg_tasks_count = pg_tasks_count.scalar()

        print(f"SQLite: {sqlite_users_count} users, {sqlite_tasks_count} tasks")
        print(f"PostgreSQL: {pg_users_count} users, {pg_tasks_count} tasks")

        # Validate counts match
        if sqlite_users_count == pg_users_count and sqlite_tasks_count == pg_tasks_count:
            print("✓ Data migration validation passed!")
            return True
        else:
            print("✗ Data migration validation failed!")
            return False

    except Exception as e:
        print(f"Error during validation: {e}")
        return False
    finally:
        await sqlite_engine.dispose()
        await pg_engine.dispose()


if __name__ == "__main__":
    # Run the migration
    asyncio.run(migrate_data_sqlite_to_postgresql())

    # Validate the migration
    asyncio.run(validate_data_migration())