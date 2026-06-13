#!/usr/bin/env python
"""Create a complete test sale with all data relationships"""

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
    # 1. Create a customer
    print("Creating customer...")
    cursor.execute("""
        INSERT INTO customers (name, phone, email, address, date_of_birth)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING *
    """, ("Jane Smith", "9876543210", "jane@example.com", "456 Oak Street", "1990-05-15"))
    customer = cursor.fetchone()
    customer_id = customer['id']
    print(f"Customer created: {customer}")
    
    # 2. Create a prescription
    print("\nCreating prescription...")
    cursor.execute("""
        INSERT INTO prescriptions (customer_id, doctor_name, prescription_date)
        VALUES (%s, %s, CURRENT_DATE)
        RETURNING *
    """, (customer_id, "Dr. James Wilson"))
    prescription = cursor.fetchone()
    prescription_id = prescription['id']
    print(f"Prescription created: {prescription}")
    
    # 3. Create an order
    print("\nCreating order...")
    cursor.execute("""
        INSERT INTO orders (customer_id, doctor_name, prescription_id, status)
        VALUES (%s, %s, %s, %s)
        RETURNING *
    """, (customer_id, "Dr. James Wilson", prescription_id, "pending"))
    order = cursor.fetchone()
    print(f"Order created: {order}")
    
    # 4. Get a medicine and its inventory
    print("\nFetching medicine and inventory...")
    cursor.execute("""
        SELECT i.*, m.medicine_name
        FROM inventory i
        LEFT JOIN medicines m ON i.medicine_id = m.id
        WHERE i.batch_id IS NOT NULL AND i.expiry_date IS NOT NULL
        LIMIT 1
    """)
    inventory_item = cursor.fetchone()
    if inventory_item:
        medicine_id = inventory_item['medicine_id']
        inventory_id = inventory_item['id']
        print(f"Inventory item: {dict(inventory_item)}")
    else:
        print("No inventory item with batch/expiry found, creating one...")
        # Get any medicine
        cursor.execute("SELECT id FROM medicines LIMIT 1")
        med = cursor.fetchone()
        medicine_id = med['id']
        # Insert inventory manually
        cursor.execute("""
            INSERT INTO inventory (medicine_id, batch_id, expiry_date, quantity, purchase_price, selling_price)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING *
        """, (medicine_id, "BATCH-123456", "2026-12-31", 100, 50.00, 100.00))
        inv = cursor.fetchone()
        inventory_id = inv['id']
        print(f"Inventory created: {dict(inv)}")
    
    # 5. Get the pharmacy
    print("\nFetching pharmacy...")
    cursor.execute("SELECT * FROM pharmacy LIMIT 1")
    pharmacy = cursor.fetchone()
    pharmacy_id = pharmacy['id']
    print(f"Pharmacy: {dict(pharmacy)}")
    
    # 6. Create the sale with all relationships
    print("\nCreating complete sale...")
    from datetime import datetime
    
    # Generate invoice number
    import time
    invoice_number = f"INV-{int(time.time() * 1000)}-{pharmacy_id}{customer_id}"
    
    cursor.execute("""
        INSERT INTO sales (
            pharmacy_id, customer_id, invoice_number, subtotal, tax, discount,
            final_amount, payment_method, generated_by_user_id
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING *
    """, (pharmacy_id, customer_id, invoice_number, 500.00, 50.00, 0, 550.00, "card", 1))
    
    sale = cursor.fetchone()
    sale_id = sale['id']
    print(f"Sale created: {dict(sale)}")
    
    # 7. Add sale items
    print("\nAdding sale items...")
    cursor.execute("""
        INSERT INTO sales_items (
            sale_id, medicine_id, inventory_id, quantity, unit_price, total_price
        ) VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING *
    """, (sale_id, medicine_id, inventory_id, 5, 100.00, 500.00))
    
    item = cursor.fetchone()
    print(f"Sale item created: {dict(item)}")
    
    # Commit the transaction
    conn.commit()
    print(f"\n✅ Complete sale created successfully!")
    print(f"Sale ID: {sale_id}")
    print(f"Invoice Number: {invoice_number}")
    print(f"Customer ID: {customer_id}")
    print(f"Pharmacy ID: {pharmacy_id}")
    print(f"\nNow generate invoice with:")
    print(f"POST /api/billing/generate-invoice/{sale_id}")
    
except Exception as e:
    conn.rollback()
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

finally:
    cursor.close()
    conn.close()
