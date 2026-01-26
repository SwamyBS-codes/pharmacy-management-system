"""Test the sales endpoint to check what data is returned"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000/api"

print("=" * 70)
print("🧪 SALES DATA API TEST")
print("=" * 70)

# Get auth token first
test_email = "swamybs272@gmail.com"
test_password = "Test@1234"

try:
    # Login to get token
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": test_email, "password": test_password},
        timeout=5
    )
    
    if login_response.status_code != 200:
        print("❌ Login failed!")
        print(login_response.json())
        exit(1)
    
    token = login_response.json()['token']
    print("✅ Login successful, got token")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Calculate date range (first day of current month to today)
    today = datetime.now()
    first_day = today.replace(day=1)
    
    # Test sales endpoint with date range
    print("\n" + "=" * 70)
    print("Testing /api/sales")
    print("=" * 70)
    print(f"Date Range: {first_day.strftime('%Y-%m-%d')} to {today.strftime('%Y-%m-%d')}")
    
    params = {
        'startDate': first_day.strftime('%Y-%m-%d'),
        'endDate': today.strftime('%Y-%m-%d'),
        'limit': 1000
    }
    
    response = requests.get(
        f"{BASE_URL}/sales",
        headers=headers,
        params=params,
        timeout=10
    )
    
    print(f"\n📊 Response Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        sales = data.get('data', [])
        pagination = data.get('pagination', {})
        
        print(f"\n✅ SUCCESS!")
        print(f"   Total Sales Records: {len(sales)}")
        print(f"   Pagination Total: {pagination.get('total', 0)}")
        
        if sales:
            print(f"\n📈 Sample Sales:")
            for sale in sales[:5]:
                created_at = sale.get('created_at', 'N/A')
                if created_at and created_at != 'N/A':
                    try:
                        date_obj = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                        month_key = date_obj.strftime('%B %Y')
                        print(f"   {created_at[:10]}: ₹{sale.get('final_amount', 0)} - Invoice: {sale.get('invoice_number')} - Month: {month_key}")
                    except:
                        print(f"   {created_at}: ₹{sale.get('final_amount', 0)} - Invoice: {sale.get('invoice_number')}")
            
            # Group by month
            monthly_sales = {}
            for sale in sales:
                created_at = sale.get('created_at')
                if created_at:
                    try:
                        date_obj = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                        month_key = date_obj.strftime('%B %Y')
                        if month_key not in monthly_sales:
                            monthly_sales[month_key] = {'sales': 0, 'orders': 0}
                        monthly_sales[month_key]['sales'] += float(sale.get('final_amount', 0))
                        monthly_sales[month_key]['orders'] += 1
                    except Exception as e:
                        print(f"   Error parsing date: {e}")
            
            print(f"\n📅 Monthly Summary:")
            for month, data in sorted(monthly_sales.items()):
                print(f"   {month}: ₹{data['sales']:.2f} ({data['orders']} orders)")
        else:
            print("\n⚠️  No sales data found for the selected period")
    else:
        print(f"\n❌ ERROR: {response.status_code}")
        print(response.json())
        
except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
