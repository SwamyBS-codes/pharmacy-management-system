#!/usr/bin/env python3
import psycopg2
from psycopg2.extras import RealDictCursor
import sys

try:
    conn = psycopg2.connect(
        host="localhost",
        database="pharmacy_db",
        user="postgres",
        password="rama"
    )
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    # Get sales records
    cur.execute('SELECT id, invoice_number, customer_id, subtotal, tax FROM sales LIMIT 5')
    rows = cur.fetchall()
    print(f"Found {len(rows)} sales records:")
    for row in rows:
        print(f"Sale ID: {row['id']}, Invoice: {row['invoice_number']}, Customer: {row['customer_id']}")
    
    # Get pharmacy data
    cur.execute('SELECT * FROM pharmacy LIMIT 1')
    pharmacy = cur.fetchone()
    if pharmacy:
        print(f"\nPharmacy: {pharmacy.get('pharmacy_name')} - {pharmacy.get('address')}")
    
    cur.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
