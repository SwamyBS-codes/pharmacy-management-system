#!/usr/bin/env python3
"""
Simple Supabase Medicines Importer
Imports medicines SQL files one at a time with visual progress
"""

import os
import psycopg2
from pathlib import Path
from dotenv import load_dotenv
import time

load_dotenv('.env.supabase')

class MedicinesImporter:
    def __init__(self):
        self.host = os.getenv('DB_HOST')
        self.port = os.getenv('DB_PORT', '5432')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.database = os.getenv('DB_NAME')
        self.conn = None
        
    def connect(self):
        """Connect to Supabase"""
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                sslmode='require'
            )
            print("✅ Connected to Supabase")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def get_count(self):
        """Get current medicines count"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM medicines;")
            count = cursor.fetchone()[0]
            cursor.close()
            return count
        except:
            return 0
    
    def import_file(self, file_path):
        """Import a single SQL file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                sql = f.read()
            
            cursor = self.conn.cursor()
            cursor.execute(sql)
            self.conn.commit()
            cursor.close()
            
            count = self.get_count()
            return True, count
        except Exception as e:
            return False, str(e)
    
    def run_interactive(self):
        """Interactive import mode"""
        if not self.connect():
            return
        
        migration_dir = Path('supabase_migration')
        files = sorted(migration_dir.glob('03_data_medicines_part*.sql'))
        
        if not files:
            print(f"❌ No medicines files found in {migration_dir}/")
            return
        
        print(f"\n📊 Found {len(files)} medicines files")
        print("=" * 80)
        
        initial_count = self.get_count()
        print(f"Starting count: {initial_count:,} medicines\n")
        
        for idx, file_path in enumerate(files, 1):
            filename = file_path.name
            success, result = self.import_file(file_path)
            
            if success:
                percent = (idx / len(files)) * 100
                print(f"[{idx:4d}/{len(files)}] {filename:<40} | "
                      f"Total: {result:,} medicines | {percent:5.1f}%")
            else:
                print(f"[{idx:4d}/{len(files)}] {filename:<40} | "
                      f"❌ Error: {str(result)[:40]}")
            
            # Show option to pause
            if idx % 100 == 0:
                response = input(f"\n⏸️  Imported {idx} files. Continue? (y/n): ")
                if response.lower() != 'y':
                    print(f"Paused at file {idx}. Resume by running script again.")
                    break
        
        final_count = self.get_count()
        imported = final_count - initial_count
        
        print("\n" + "=" * 80)
        print(f"✅ Import Complete!")
        print(f"   Before: {initial_count:,}")
        print(f"   After: {final_count:,}")
        print(f"   Imported: {imported:,} new medicines")
        
        self.conn.close()
    
    def import_from_file(self, start_file_number):
        """Import starting from specific file number"""
        if not self.connect():
            return
        
        migration_dir = Path('supabase_migration')
        files = sorted(migration_dir.glob('03_data_medicines_part*.sql'))
        files = [f for f in files if int(f.stem.split('part')[1]) >= start_file_number]
        
        print(f"\n📊 Importing {len(files)} files starting from part{start_file_number}")
        print("=" * 80)
        
        initial_count = self.get_count()
        print(f"Starting count: {initial_count:,}\n")
        
        for idx, file_path in enumerate(files, 1):
            success, result = self.import_file(file_path)
            
            if success:
                print(f"✅ {file_path.name} | Total: {result:,}")
            else:
                print(f"❌ {file_path.name} | Error: {result}")
        
        final_count = self.get_count()
        print(f"\nFinal count: {final_count:,}")
        self.conn.close()

if __name__ == '__main__':
    import sys
    
    importer = MedicinesImporter()
    
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        # Resume from specific file
        importer.import_from_file(int(sys.argv[1]))
    else:
        # Interactive mode
        importer.run_interactive()
