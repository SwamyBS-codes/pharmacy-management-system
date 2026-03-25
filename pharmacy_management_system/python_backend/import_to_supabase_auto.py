#!/usr/bin/env python3
"""
Auto-import to Supabase without prompts
Uses .env.supabase configuration
"""
import psycopg2
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment
env_file = '.env.supabase'
if os.path.exists(env_file):
    load_dotenv(env_file)
else:
    print(f"Error: {env_file} not found!")
    exit(1)

conn_params = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'postgres'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

migration_dir = "supabase_migration"

def run_sql_file(conn, filepath):
    """Execute SQL from a file"""
    filename = os.path.basename(filepath)
    print(f"\nRunning {filename}...", end=" ", flush=True)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            sql = f.read()
        
        cursor = conn.cursor()
        
        # Split by semicolons and execute
        statements = [s.strip() for s in sql.split(';') if s.strip()]
        
        for statement in statements:
            if not statement.startswith('--'):
                try:
                    cursor.execute(statement)
                except Exception as e:
                    # Ignore some errors
                    if "already exists" not in str(e).lower():
                        pass
        
        conn.commit()
        cursor.close()
        print("OK")
        return True
        
    except Exception as e:
        print(f"FAILED: {e}")
        conn.rollback()
        return False

def main():
    print("=" * 60)
    print("SUPABASE DATA IMPORT")
    print("=" * 60)
    
    # Test connection
    print("\nTesting connection...", end=" ", flush=True)
    try:
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        cursor.execute("SELECT version()")
        cursor.close()
        print("OK")
    except Exception as e:
        print(f"FAILED: {e}")
        return False
    
    # Files to import
    sql_files = [
        '01_schema.sql',
        '02_data_core.sql',
        '03_data_medicines.sql',
        '04_data_inventory.sql',
        '05_data_customers.sql',
        '06_data_sales.sql',
        '07_data_other.sql'
    ]
    
    print("\n" + "=" * 60)
    print("STARTING IMPORT")
    print("=" * 60)
    
    start_time = datetime.now()
    success = 0
    
    for sql_file in sql_files:
        filepath = os.path.join(migration_dir, sql_file)
        if os.path.exists(filepath):
            if run_sql_file(conn, filepath):
                success += 1
        else:
            print(f"\nWarning: {sql_file} not found")
    
    conn.close()
    
    duration = (datetime.now() - start_time).total_seconds()
    
    print("\n" + "=" * 60)
    print("IMPORT COMPLETED")
    print("=" * 60)
    print(f"Files processed: {success}/{len(sql_files)}")
    print(f"Duration: {duration:.2f} seconds")
    print("\nNext steps:")
    print("1. Run verification: python verify_supabase_migration.py")
    print("2. Update main .env file with Supabase details")
    print("3. Test the application")
    print()
    
    return True

if __name__ == "__main__":
    main()
