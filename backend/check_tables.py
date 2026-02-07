from sqlalchemy import create_engine, inspect
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

try:
    from src.database.connection import settings
    engine = create_engine(settings.database_url)
    inspector = inspect(engine)
    print(f"Tables in {settings.database_url}: {inspector.get_table_names()}")
except Exception as e:
    print(f"Error: {e}")
