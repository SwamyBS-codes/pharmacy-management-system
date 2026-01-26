#!/usr/bin/env python
"""Create test out-of-stock inventory items"""

import psycopg2
from psycopg2 import extras
from config import Config

def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            host=Config.DB_HOST,
            port=Config.DB_PORT
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

conn = get_db_connection()
if not conn:
    exit(1)

cursor = conn.cursor(cursor_factory=extras.RealDictCursor)

try:
    print("Creating out-of-stock inventory items for testing...")
    
    # Get some medicines
    cursor.execute("SELECT id, medicine_name FROM medicines LIMIT 5")
    medicines = cursor.fetchall()
    
    if not medicines:
        print("No medicines found in database!")
        exit(1)
    
    print(f"Found {len(medicines)} medicines")
    
    # Create inventory items with 0 or negative quantity
    for i, med in enumerate(medicines):
        med_id = med['id']
        med_name = med['medicine_name']
        batch_id = f"BATCH-OOS-{i+1:03d}"
        
        print(f"\nCreating out-of-stock item for: {med_name}")
        
        # Check if inventory exists for this medicine
        cursor.execute(
            "SELECT id FROM inventory WHERE medicine_id = %s LIMIT 1",
            (med_id,)
        )
        existing = cursor.fetchone()
        
        if existing:
            # Update existing to 0
            cursor.execute(
                "UPDATE inventory SET quantity = 0, batch_id = %s WHERE medicine_id = %s",
                (batch_id, med_id)
            )
            print(f"  ✓ Updated existing inventory to quantity=0")
        else:
            # Create new out-of-stock inventory
            cursor.execute(
                """
                INSERT INTO inventory (medicine_id, batch_id, quantity, expiry_date, 
                                      purchase_price, selling_price)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (med_id, batch_id, 0, '2025-12-31', 50.0, 100.0)
            )
            print(f"  ✓ Created new inventory with quantity=0")
    
    # Also create some with negative quantity (over-sold)
    if len(medicines) > 0:
        med = medicines[0]
        batch_id = f"BATCH-OVERSOLD-001"
        cursor.execute(
            "UPDATE inventory SET quantity = -10, batch_id = %s WHERE medicine_id = %s",
            (batch_id, med['id'])
        )
        print(f"\n✓ Created over-sold item: {med['medicine_name']} with quantity=-10")
    
    conn.commit()
    
    # Verify
    print("\n" + "="*80)
    print("Verifying out-of-stock items created...")
    cursor.execute(
        """
        SELECT i.id, i.medicine_id, i.batch_id, i.quantity, m.medicine_name, m.manufacturer
        FROM inventory i
        LEFT JOIN medicines m ON i.medicine_id = m.id
        WHERE i.quantity <= 0
        ORDER BY m.medicine_name
        """
    )
    
    results = cursor.fetchall()
    print(f"\nFound {len(results)} out-of-stock/low-stock items:\n")
    for r in results:
        print(f"  • {r['medicine_name']}")
        print(f"    Batch: {r['batch_id']}")
        print(f"    Quantity: {r['quantity']}")
        print(f"    Manufacturer: {r['manufacturer']}")
        print()
    
    print("✅ Test out-of-stock items created successfully!")
    
except Exception as e:
    conn.rollback()
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

finally:
    cursor.close()
    conn.close()
