"""
Initialize PostgreSQL schema by executing schema.sql via psycopg2.
Run with the backend venv Python: python initialize_db.py
"""
import os
import sys
import logging

# Ensure module imports from current directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db import get_db_connection, release_db_connection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCHEMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schema.sql')


def run_schema():
    conn = None
    try:
        logger.info(f"Loading schema from: {SCHEMA_PATH}")
        with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
            sql = f.read()
        conn = get_db_connection()
        # Autocommit to allow DDL/DO blocks to run cleanly
        conn.autocommit = True
        cur = conn.cursor()
        logger.info("Executing schema SQL... This may take a moment.")
        cur.execute(sql)
        cur.close()
        logger.info("✅ Schema applied successfully.")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to apply schema: {e}")
        return False
    finally:
        if conn:
            release_db_connection(conn)


if __name__ == '__main__':
    ok = run_schema()
    sys.exit(0 if ok else 1)
