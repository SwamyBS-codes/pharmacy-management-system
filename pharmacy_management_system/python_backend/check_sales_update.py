"""
Check if sales are being created and updated in the database
"""
import sys
sys.path.insert(0, '.')

from db import execute_query
import json
from datetime import datetime, timedelta

print("=" * 80)
print("🔍 SALES DATA CHECK")
print("=" * 80)

# 1. Check total sales count
print("\n1. Total Sales in Database:")
total_query = "SELECT COUNT(*) as count FROM sales"
result = execute_query(total_query, fetch_one=True)
total_sales = result['count'] if result else 0
print(f"   Total sales records: {total_sales}")

# 2. Check today's sales
print("\n2. Today's Sales:")
today_query = """
    SELECT DATE(created_at) as date, COUNT(*) as count, SUM(final_amount) as total
    FROM sales
    WHERE DATE(created_at) = CURRENT_DATE
    GROUP BY DATE(created_at)
"""
today_result = execute_query(today_query, fetch_one=True)
if today_result:
    print(f"   Date: {today_result['date']}")
    print(f"   Count: {today_result['count']}")
    print(f"   Total: ₹{today_result['total']}")
else:
    print("   No sales today")

# 3. Check recent sales
print("\n3. Recent Sales (Last 5):")
recent_query = """
    SELECT id, created_at, final_amount, invoice_number
    FROM sales
    ORDER BY created_at DESC
    LIMIT 5
"""
recent = execute_query(recent_query)
for sale in recent:
    print(f"   ID: {sale['id']}, Invoice: {sale['invoice_number']}, Amount: ₹{sale['final_amount']}, Created: {sale['created_at']}")

# 4. Check daily sales stats
print("\n4. Daily Sales Stats (Last 7 Days):")
stats_query = """
    SELECT DATE(created_at) as date, COUNT(*) as transactions, SUM(final_amount) as sales
    FROM sales
    WHERE DATE(created_at) >= CURRENT_DATE - INTERVAL '7 days'
    GROUP BY DATE(created_at)
    ORDER BY date DESC
"""
stats = execute_query(stats_query)
for stat in stats:
    print(f"   {stat['date']}: {stat['transactions']} transactions, ₹{stat['sales']} total")

# 5. Check if sales items are being created
print("\n5. Sales Items Check:")
items_query = "SELECT COUNT(*) as count FROM sales_items"
items_result = execute_query(items_query, fetch_one=True)
print(f"   Total sales items: {items_result['count'] if items_result else 0}")

print("\n" + "=" * 80)
print("✅ Check complete!")
print("=" * 80)
