#!/usr/bin/env python3
"""Update medicine prices with varied values"""
from db import get_db_connection, release_db_connection
from psycopg2 import extras
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("=" * 80)
print("💰 UPDATING MEDICINE PRICES WITH VARIED VALUES")
print("=" * 80)

conn = None
try:
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
    
    # Get all medicines
    cursor.execute("SELECT id, medicine_name, category FROM medicines ORDER BY id")
    medicines = cursor.fetchall()
    print(f"\n📊 Found {len(medicines)} medicines to update\n")
    
    # Define price ranges based on category/type
    price_map = {
        'Tablet': [50, 75, 100, 125, 150, 175, 200, 250, 300, 350],
        'Capsule': [60, 80, 110, 140, 160, 180, 210, 260, 310, 360],
        'Syrup': [80, 120, 150, 180, 220, 260, 300, 350, 400, 450],
        'Injection': [150, 200, 250, 300, 350, 400, 450, 500, 550, 600],
        'Cream': [70, 100, 130, 160, 190, 220, 250, 300, 350, 400],
        'Gel': [60, 90, 120, 150, 180, 210, 240, 280, 320, 360],
        'Lotion': [100, 130, 160, 190, 220, 250, 280, 320, 360, 400],
        'Ointment': [80, 110, 140, 170, 200, 230, 260, 300, 340, 380],
        'Oil': [70, 100, 130, 160, 190, 220, 250, 290, 330, 370],
        'Powder': [50, 75, 100, 125, 150, 175, 200, 240, 280, 320],
    }
    
    updated_count = 0
    updates = []
    
    for i, medicine in enumerate(medicines):
        med_id = medicine['id']
        med_name = medicine['medicine_name']
        category = medicine['category'] or 'Tablet'
        
        # Get price range for category
        prices = price_map.get(category, [50, 75, 100, 125, 150, 175, 200, 250, 300, 350])
        
        # Use modulo to distribute prices
        price_index = i % len(prices)
        new_price = prices[price_index]
        
        # Update medicine price
        cursor.execute("UPDATE medicines SET price = %s WHERE id = %s", (new_price, med_id))
        
        if i < 15:  # Keep track of first 15 for display
            updates.append({
                'id': med_id,
                'name': med_name,
                'category': category,
                'price': new_price
            })
        
        updated_count += 1
        
        # Print every 1000th update
        if (i + 1) % 1000 == 0:
            print(f"✓ Updated {updated_count} medicines...")
    
    conn.commit()
    cursor.close()
    
    print(f"\n✅ Successfully updated {updated_count} medicines with varied prices!\n")
    
    # Show sample of updates
    print("Sample updates:")
    print("-" * 80)
    for update in updates:
        print(f"ID {update['id']}: {update['name'][:40]:<40} | {update['category']:<12} | ₹{update['price']}")
    
    if updated_count > 15:
        print(f"... and {updated_count - 15} more medicines")
    
    print("\n📈 Price distribution by category:")
    print("-" * 80)
    
    # Get price statistics
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
    for category in sorted(price_map.keys()):
        cursor.execute("""
            SELECT COUNT(*) as count, 
                   AVG(price) as avg_price,
                   MIN(price) as min_price,
                   MAX(price) as max_price
            FROM medicines 
            WHERE category = %s
        """, (category,))
        stats = cursor.fetchone()
        if stats and stats['count'] > 0:
            print(f"{category:<15} | Count: {stats['count']:<4} | Avg: ₹{stats['avg_price']:>7.2f} | Range: ₹{stats['min_price']}-₹{stats['max_price']}")
    
    cursor.close()
    
    print("\n" + "=" * 80)
    print("💰 All medicines now have varied prices!")
    print("=" * 80)

except Exception as e:
    if conn:
        conn.rollback()
    logger.error(f"Error updating medicines: {e}")
    print(f"\n❌ Error: {e}")
finally:
    if conn:
        release_db_connection(conn)
