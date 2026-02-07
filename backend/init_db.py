"""
Script to initialize the database tables for the Todo application.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.database.connection import engine, Base, settings
from sqlalchemy_utils import database_exists, create_database

def init_db():
    print(f"Connecting to database: {settings.database_url}")

    try:
        # Check if database exists, create if it doesn't
        if not database_exists(settings.database_url):
            print("Database does not exist, creating it...")
            create_database(settings.database_url)
        else:
            print("Database already exists.")

        # Create all tables
        print("Creating tables...")
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully!")

    except Exception as e:
        print(f"Error initializing database: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    init_db()