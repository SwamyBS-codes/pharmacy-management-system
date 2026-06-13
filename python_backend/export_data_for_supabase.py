"""
Export local PostgreSQL data for Supabase migration
Creates SQL dump files that can be imported to Supabase
"""
import psycopg2
import os
from config import Config
from datetime import datetime

# Create migration directory
MIGRATION_DIR = "supabase_migration"
os.makedirs(MIGRATION_DIR, exist_ok=True)

def export_schema():
    """Export database schema (without data)"""
    print("📋 Exporting schema...")
    
    # Read the schema.sql file
    with open('schema.sql', 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    
    # Write to migration folder
    output_file = os.path.join(MIGRATION_DIR, '01_schema.sql')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("-- Pharmacy Management System - Database Schema\n")
        f.write(f"-- Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("-- Deploy this to Supabase SQL Editor\n\n")
        f.write(schema_sql)
    
    print(f"✅ Schema exported to {output_file}")

def export_table_data(cursor, table_name, output_file, batch_size=1000):
    """Export data from a table as INSERT statements"""
    print(f"📊 Exporting {table_name}...")
    
    # Get column names
    cursor.execute(f"""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = '{table_name}' 
        ORDER BY ordinal_position
    """)
    columns = [row[0] for row in cursor.fetchall()]
    column_list = ', '.join(columns)
    
    # Get total count
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    total_count = cursor.fetchone()[0]
    
    if total_count == 0:
        print(f"⚠️  {table_name} is empty, skipping...")
        return
    
    print(f"   Found {total_count} records")
    
    # Export data in batches
    with open(output_file, 'a', encoding='utf-8') as f:
        f.write(f"\n-- ============================================\n")
        f.write(f"-- {table_name.upper()} DATA ({total_count} records)\n")
        f.write(f"-- ============================================\n\n")
        
        offset = 0
        while offset < total_count:
            cursor.execute(f"SELECT * FROM {table_name} ORDER BY id LIMIT {batch_size} OFFSET {offset}")
            rows = cursor.fetchall()
            
            if rows:
                # Write INSERT statements
                f.write(f"-- Batch {offset//batch_size + 1} ({len(rows)} records)\n")
                f.write(f"INSERT INTO {table_name} ({column_list}) VALUES\n")
                
                for i, row in enumerate(rows):
                    # Format values
                    values = []
                    for val in row:
                        if val is None:
                            values.append('NULL')
                        elif isinstance(val, str):
                            # Escape single quotes
                            escaped = val.replace("'", "''")
                            values.append(f"'{escaped}'")
                        elif isinstance(val, (int, float)):
                            values.append(str(val))
                        elif isinstance(val, bool):
                            values.append('TRUE' if val else 'FALSE')
                        else:
                            # Handle dates, timestamps, etc.
                            values.append(f"'{val}'")
                    
                    value_str = ', '.join(values)
                    if i < len(rows) - 1:
                        f.write(f"  ({value_str}),\n")
                    else:
                        f.write(f"  ({value_str})\n")
                
                f.write("ON CONFLICT (id) DO UPDATE SET ")
                update_cols = [f"{col} = EXCLUDED.{col}" for col in columns if col != 'id']
                f.write(", ".join(update_cols))
                f.write(";\n\n")
            
            offset += batch_size
            print(f"   Processed {min(offset, total_count)}/{total_count} records...")
    
    print(f"✅ {table_name} exported successfully")

def export_all_data():
    """Export all table data"""
    print("\n🚀 Starting data export for Supabase migration...\n")
    
    try:
        # Connect to local database
        conn = psycopg2.connect(**Config.get_db_connection_string())
        cursor = conn.cursor()
        
        # Export schema first
        export_schema()
        
        # Tables to export (in order to handle foreign keys)
        tables_order = [
            # Core tables
            ('pharmacy', '02_data_core.sql'),
            ('users', '02_data_core.sql'),
            ('suppliers', '02_data_core.sql'),
            
            # Medicines (largest table usually)
            ('medicines', '03_data_medicines.sql'),
            
            # Inventory and customers
            ('inventory', '04_data_inventory.sql'),
            ('customers', '05_data_customers.sql'),
            
            # Sales and related
            ('sales', '06_data_sales.sql'),
            ('sales_items', '06_data_sales.sql'),
            
            # Other tables
            ('orders', '07_data_other.sql'),
            ('prescriptions', '07_data_other.sql'),
            ('auth_tokens', '07_data_other.sql'),
        ]
        
        # Clear output files
        output_files = set([table[1] for table in tables_order])
        for output_file in output_files:
            filepath = os.path.join(MIGRATION_DIR, output_file)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"-- Pharmacy Management System - Data Export\n")
                f.write(f"-- Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"-- File: {output_file}\n\n")
                f.write("-- Disable triggers temporarily for faster import\n")
                f.write("SET session_replication_role = replica;\n\n")
        
        # Export each table
        for table_name, output_file in tables_order:
            filepath = os.path.join(MIGRATION_DIR, output_file)
            try:
                export_table_data(cursor, table_name, filepath)
            except Exception as e:
                print(f"⚠️  Error exporting {table_name}: {e}")
                continue
        
        # Add sequence resets to each file
        for output_file in output_files:
            filepath = os.path.join(MIGRATION_DIR, output_file)
            with open(filepath, 'a', encoding='utf-8') as f:
                f.write("\n-- Re-enable triggers\n")
                f.write("SET session_replication_role = DEFAULT;\n\n")
                f.write("-- Update sequences to prevent ID conflicts\n")
                f.write("""
DO $$
DECLARE
    seq_name TEXT;
    max_id INTEGER;
BEGIN
    FOR seq_name IN 
        SELECT sequence_name 
        FROM information_schema.sequences 
        WHERE sequence_schema = 'public'
    LOOP
        EXECUTE format('SELECT setval(%L, (SELECT COALESCE(MAX(id), 0) + 1 FROM %I))', 
                      seq_name, 
                      replace(seq_name, '_id_seq', ''));
    END LOOP;
END $$;
""")
        
        cursor.close()
        conn.close()
        
        print("\n" + "="*60)
        print("✅ EXPORT COMPLETED SUCCESSFULLY!")
        print("="*60)
        print(f"\n📁 Migration files created in: {MIGRATION_DIR}/")
        print("\nNext steps:")
        print("1. Go to your Supabase project")
        print("2. Open SQL Editor")
        print("3. Run files in order:")
        print("   - 01_schema.sql")
        print("   - 02_data_core.sql")
        print("   - 03_data_medicines.sql")
        print("   - 04_data_inventory.sql")
        print("   - 05_data_customers.sql")
        print("   - 06_data_sales.sql")
        print("   - 07_data_other.sql")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ Error during export: {e}")
        print("Please check your database connection and try again.")
        return False
    
    return True

if __name__ == "__main__":
    export_all_data()
