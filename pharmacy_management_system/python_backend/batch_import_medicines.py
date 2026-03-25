#!/usr/bin/env python3
"""
Supabase Medicines Batch Import Tool
Imports split medicines SQL files to Supabase with progress tracking
"""

import os
import sys
import time
from pathlib import Path
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.supabase')

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

def get_connection():
    """Create database connection with SSL"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            sslmode='require'
        )
        return conn
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return None

def import_file(conn, file_path, file_number, total_files):
    """Import a single SQL file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        cursor = conn.cursor()
        cursor.execute(sql_content)
        conn.commit()
        cursor.close()
        
        # Get current count
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM medicines;")
        count = cursor.fetchone()[0]
        cursor.close()
        
        percent = (file_number / total_files) * 100
        print(f"✅ [{file_number}/{total_files}] {Path(file_path).name:<50} | "
              f"Total medicines: {count:,} | {percent:.1f}%")
        return True
        
    except Exception as e:
        print(f"❌ [{file_number}/{total_files}] {Path(file_path).name:<50} | Error: {str(e)[:60]}")
        return False

def main():
    """Main import loop"""
    migration_dir = Path('supabase_migration')
    files = sorted(migration_dir.glob('03_data_medicines_part*.sql'))
    
    if not files:
        print("❌ No medicines files found in supabase_migration/")
        sys.exit(1)
    
    print(f"\n🔄 Found {len(files)} medicines files to import")
    print("=" * 120)
    
    # Connect to database
    conn = get_connection()
    if not conn:
        sys.exit(1)
    
    # Get initial count
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM medicines;")
    initial_count = cursor.fetchone()[0]
    cursor.close()
    print(f"📊 Initial medicines count: {initial_count:,}\n")
    
    # Import all files
    successful = 0
    failed = 0
    start_time = time.time()
    
    for idx, file_path in enumerate(files, 1):
        if import_file(conn, file_path, idx, len(files)):
            successful += 1
        else:
            failed += 1
        
        # Small pause between imports
        if idx < len(files):
            time.sleep(0.1)
    
    # Final summary
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM medicines;")
    final_count = cursor.fetchone()[0]
    cursor.close()
    
    elapsed = time.time() - start_time
    imported = final_count - initial_count
    
    print("\n" + "=" * 120)
    print(f"✅ Import Complete!")
    print(f"   Successful: {successful}/{len(files)}")
    print(f"   Failed: {failed}/{len(files)}")
    print(f"   Time elapsed: {elapsed/60:.1f} minutes")
    print(f"   Records before: {initial_count:,}")
    print(f"   Records after: {final_count:,}")
    print(f"   Records imported: {imported:,}")
    print(f"   Records/minute: {imported/(elapsed/60):.0f}")
    
    conn.close()

if __name__ == '__main__':
    main()
