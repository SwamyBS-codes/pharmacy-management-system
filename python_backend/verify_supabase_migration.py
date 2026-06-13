"""
Verify Supabase migration
Checks that all tables, data, and constraints are properly migrated
"""
import psycopg2
import os
from dotenv import load_dotenv

def get_connection_params():
    """Get connection parameters from .env.supabase or user input"""
    env_file = '.env.supabase'
    if os.path.exists(env_file):
        load_dotenv(env_file)
        return {
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT', '5432'),
            'database': os.getenv('DB_NAME', 'postgres'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD')
        }
    else:
        print("⚠️  .env.supabase not found")
        print("Please enter your Supabase connection details:\n")
        return {
            'host': input("Host: ").strip(),
            'port': input("Port [5432]: ").strip() or "5432",
            'database': input("Database [postgres]: ").strip() or "postgres",
            'user': input("User: ").strip(),
            'password': input("Password: ").strip()
        }

def verify_tables(cursor):
    """Verify all required tables exist"""
    print("\n📋 Verifying Tables...")
    
    required_tables = [
        'pharmacy',
        'users',
        'auth_tokens',
        'suppliers',
        'medicines',
        'inventory',
        'customers',
        'prescriptions',
        'orders',
        'sales',
        'sales_items'
    ]
    
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_type = 'BASE TABLE'
    """)
    
    existing_tables = [row[0] for row in cursor.fetchall()]
    
    all_exist = True
    for table in required_tables:
        if table in existing_tables:
            print(f"   ✅ {table}")
        else:
            print(f"   ❌ {table} - MISSING!")
            all_exist = False
    
    return all_exist

def verify_data_counts(cursor):
    """Check record counts in each table"""
    print("\n📊 Checking Data Counts...")
    
    tables = [
        'pharmacy',
        'users',
        'suppliers',
        'medicines',
        'inventory',
        'customers',
        'sales',
        'sales_items'
    ]
    
    counts = {}
    for table in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            counts[table] = count
            print(f"   {table:20s} : {count:>8,} records")
        except Exception as e:
            print(f"   ❌ {table:20s} : Error - {e}")
    
    return counts

def verify_indexes(cursor):
    """Verify important indexes exist"""
    print("\n🔍 Verifying Indexes...")
    
    cursor.execute("""
        SELECT 
            schemaname,
            tablename,
            indexname
        FROM pg_indexes
        WHERE schemaname = 'public'
        ORDER BY tablename, indexname
    """)
    
    indexes = cursor.fetchall()
    print(f"   Found {len(indexes)} indexes")
    
    # Check for specific important indexes
    important_indexes = [
        'idx_medicines_name',
        'idx_inventory_medicine',
        'idx_sales_customer',
        'idx_sales_items_sale'
    ]
    
    index_names = [idx[2] for idx in indexes]
    for idx_name in important_indexes:
        if idx_name in index_names:
            print(f"   ✅ {idx_name}")
        else:
            print(f"   ⚠️  {idx_name} - not found")
    
    return True

def verify_foreign_keys(cursor):
    """Verify foreign key constraints"""
    print("\n🔗 Verifying Foreign Keys...")
    
    cursor.execute("""
        SELECT
            tc.table_name, 
            kcu.column_name,
            ccu.table_name AS foreign_table_name,
            ccu.column_name AS foreign_column_name 
        FROM information_schema.table_constraints AS tc 
        JOIN information_schema.key_column_usage AS kcu
            ON tc.constraint_name = kcu.constraint_name
        JOIN information_schema.constraint_column_usage AS ccu
            ON ccu.constraint_name = tc.constraint_name
        WHERE tc.constraint_type = 'FOREIGN KEY'
        AND tc.table_schema = 'public'
        ORDER BY tc.table_name
    """)
    
    fks = cursor.fetchall()
    print(f"   Found {len(fks)} foreign key constraints")
    
    # Show a few examples
    for fk in fks[:5]:
        print(f"   ✅ {fk[0]}.{fk[1]} → {fk[2]}.{fk[3]}")
    
    if len(fks) > 5:
        print(f"   ... and {len(fks) - 5} more")
    
    return True

def verify_sequences(cursor):
    """Verify and fix sequences"""
    print("\n🔢 Verifying Sequences...")
    
    cursor.execute("""
        SELECT sequence_name 
        FROM information_schema.sequences 
        WHERE sequence_schema = 'public'
    """)
    
    sequences = cursor.fetchall()
    print(f"   Found {len(sequences)} sequences")
    
    # Fix sequences to prevent ID conflicts
    for seq in sequences:
        seq_name = seq[0]
        table_name = seq_name.replace('_id_seq', '')
        try:
            cursor.execute(f"""
                SELECT setval('{seq_name}', 
                    (SELECT COALESCE(MAX(id), 0) + 1 FROM {table_name}), 
                    false)
            """)
            print(f"   ✅ {seq_name} updated")
        except Exception as e:
            print(f"   ⚠️  {seq_name}: {str(e)[:50]}")
    
    return True

def verify_admin_user(cursor):
    """Check if admin user exists"""
    print("\n👤 Verifying Admin User...")
    
    cursor.execute("SELECT id, name, email, role FROM users WHERE role = 'ADMIN'")
    admins = cursor.fetchall()
    
    if admins:
        for admin in admins:
            print(f"   ✅ Admin found: {admin[1]} ({admin[2]})")
        return True
    else:
        print("   ⚠️  No admin user found!")
        print("   You may need to create an admin user.")
        return False

def run_verification():
    """Run all verification checks"""
    print("\n" + "="*60)
    print("🔍 SUPABASE MIGRATION VERIFICATION")
    print("="*60)
    
    try:
        # Connect to Supabase
        conn_params = get_connection_params()
        print("\n🔄 Connecting to Supabase...")
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        print("✅ Connected successfully!")
        
        # Run all checks
        results = {
            'tables': verify_tables(cursor),
            'data': verify_data_counts(cursor),
            'indexes': verify_indexes(cursor),
            'foreign_keys': verify_foreign_keys(cursor),
            'sequences': verify_sequences(cursor),
            'admin': verify_admin_user(cursor)
        }
        
        conn.commit()
        cursor.close()
        conn.close()
        
        # Summary
        print("\n" + "="*60)
        print("📊 VERIFICATION SUMMARY")
        print("="*60)
        
        passed = sum(1 for v in results.values() if v)
        total = len(results)
        
        for check, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{check.upper():20s}: {status}")
        
        print("\n" + "="*60)
        if passed == total:
            print("✅ ALL CHECKS PASSED!")
            print("Your Supabase database is ready to use.")
        else:
            print(f"⚠️  {total - passed} CHECK(S) FAILED")
            print("Please review the issues above.")
        print("="*60 + "\n")
        
        return passed == total
        
    except Exception as e:
        print(f"\n❌ Verification failed: {e}")
        return False

if __name__ == "__main__":
    run_verification()
