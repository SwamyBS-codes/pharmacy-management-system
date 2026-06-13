"""
Import data to Supabase database
Runs the exported SQL files against your Supabase instance
"""
import psycopg2
import os
from datetime import datetime

def get_supabase_connection():
    """Get Supabase database connection from environment or user input"""
    print("\n🔐 Supabase Connection Setup")
    print("="*60)
    
    # Try to load from .env.supabase
    env_file = '.env.supabase'
    if os.path.exists(env_file):
        print(f"Found {env_file}")
        use_env = input("Use settings from .env.supabase? (Y/n): ").strip().lower()
        if use_env != 'n':
            from dotenv import load_dotenv
            load_dotenv(env_file)
            return {
                'host': os.getenv('DB_HOST'),
                'port': os.getenv('DB_PORT', '5432'),
                'database': os.getenv('DB_NAME', 'postgres'),
                'user': os.getenv('DB_USER'),
                'password': os.getenv('DB_PASSWORD')
            }
    
    # Manual input
    print("\nEnter your Supabase connection details:")
    print("(Find these in Supabase Dashboard → Settings → Database)")
    print()
    
    host = input("Host (db.xxxxx.supabase.co): ").strip()
    port = input("Port [5432]: ").strip() or "5432"
    database = input("Database [postgres]: ").strip() or "postgres"
    user = input("User (postgres.xxxxx): ").strip()
    password = input("Password: ").strip()
    
    return {
        'host': host,
        'port': port,
        'database': database,
        'user': user,
        'password': password
    }

def test_connection(conn_params):
    """Test the database connection"""
    print("\n🔄 Testing connection to Supabase...")
    try:
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        cursor.execute("SELECT version()")
        version = cursor.fetchone()[0]
        print(f"✅ Connected successfully!")
        print(f"   PostgreSQL version: {version[:50]}...")
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def run_sql_file(conn, filepath):
    """Execute SQL from a file"""
    filename = os.path.basename(filepath)
    print(f"\n📄 Running {filename}...")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            sql = f.read()
        
        cursor = conn.cursor()
        
        # Split by semicolons and execute each statement
        statements = sql.split(';\n')
        total = len([s for s in statements if s.strip()])
        
        for i, statement in enumerate(statements):
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                try:
                    cursor.execute(statement)
                    if i % 100 == 0 and i > 0:
                        print(f"   Processed {i}/{total} statements...")
                except Exception as e:
                    # Some statements might fail (like DROP TABLE IF NOT EXISTS)
                    # Only show critical errors
                    if "already exists" not in str(e):
                        print(f"   Warning: {str(e)[:100]}")
        
        conn.commit()
        cursor.close()
        print(f"✅ {filename} completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error running {filename}: {e}")
        conn.rollback()
        return False

def import_to_supabase():
    """Main import function"""
    print("\n" + "="*60)
    print("🚀 SUPABASE DATA IMPORT")
    print("="*60)
    
    # Check if migration files exist
    migration_dir = "supabase_migration"
    if not os.path.exists(migration_dir):
        print(f"\n❌ Migration directory '{migration_dir}' not found!")
        print("Please run 'export_data_for_supabase.py' first.")
        return False
    
    # Get connection details
    conn_params = get_supabase_connection()
    
    # Test connection
    if not test_connection(conn_params):
        print("\n❌ Cannot proceed without a valid connection.")
        return False
    
    # Confirm before proceeding
    print("\n⚠️  WARNING: This will import data to your Supabase database.")
    confirm = input("Continue? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("Import cancelled.")
        return False
    
    # Connect to Supabase
    try:
        conn = psycopg2.connect(**conn_params)
        
        # Files to import in order
        sql_files = [
            '01_schema.sql',
            '02_data_core.sql',
            '03_data_medicines.sql',
            '04_data_inventory.sql',
            '05_data_customers.sql',
            '06_data_sales.sql',
            '07_data_other.sql'
        ]
        
        print("\n" + "="*60)
        print("📊 STARTING IMPORT")
        print("="*60)
        start_time = datetime.now()
        
        success_count = 0
        for sql_file in sql_files:
            filepath = os.path.join(migration_dir, sql_file)
            if os.path.exists(filepath):
                if run_sql_file(conn, filepath):
                    success_count += 1
            else:
                print(f"⚠️  File not found: {sql_file}, skipping...")
        
        conn.close()
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print("\n" + "="*60)
        print("✅ IMPORT COMPLETED!")
        print("="*60)
        print(f"Files processed: {success_count}/{len(sql_files)}")
        print(f"Duration: {duration:.2f} seconds")
        print("\nNext steps:")
        print("1. Run 'verify_supabase_migration.py' to verify the import")
        print("2. Update your .env file with Supabase connection details")
        print("3. Test your application with the new database")
        print()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Import failed: {e}")
        return False

if __name__ == "__main__":
    import_to_supabase()
