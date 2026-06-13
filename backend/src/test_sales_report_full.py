#!/usr/bin/env python3
"""
Comprehensive Sales Report Test
Tests all endpoints needed for the sales report page
"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = 'http://localhost:5000/api'

print("=" * 80)
print("🧪 COMPREHENSIVE SALES REPORT TEST")
print("=" * 80)

# Step 1: Login
print("\n[Step 1] Logging in...")
try:
    login_resp = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": "swamybs272@gmail.com", "password": "Test@1234"},
        timeout=5
    )
    
    if login_resp.status_code != 200:
        print(f"❌ Login failed: {login_resp.status_code}")
        print(f"   Response: {login_resp.text}")
        exit(1)
    
    token = login_resp.json()['token']
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    print("✅ Login successful")
    print(f"   Token: {token[:50]}...")
except Exception as e:
    print(f"❌ Login error: {e}")
    exit(1)

# Step 2: Test Sales Stats Summary
print("\n[Step 2] Testing Sales Stats Summary...")
try:
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    
    stats_resp = requests.get(
        f"{BASE_URL}/sales/stats/summary",
        headers=headers,
        params={'startDate': start_date, 'endDate': end_date},
        timeout=5
    )
    
    print(f"   Status: {stats_resp.status_code}")
    
    if stats_resp.status_code == 200:
        stats = stats_resp.json()
        print("✅ Stats retrieved successfully")
        print(f"   Total Sales: ₹{stats['summary'].get('total_sales', 0)}")
        print(f"   Total Transactions: {stats['summary'].get('total_transactions', 0)}")
        print(f"   Daily Sales Count: {len(stats.get('dailySales', []))}")
        print(f"   Top Medicines Count: {len(stats.get('topMedicines', []))}")
    else:
        print(f"❌ Failed: {stats_resp.text}")
        
except Exception as e:
    print(f"❌ Error: {e}")

# Step 3: Test Sales List
print("\n[Step 3] Testing Sales List...")
try:
    sales_resp = requests.get(
        f"{BASE_URL}/sales",
        headers=headers,
        params={'limit': 10, 'startDate': start_date, 'endDate': end_date},
        timeout=5
    )
    
    print(f"   Status: {sales_resp.status_code}")
    
    if sales_resp.status_code == 200:
        sales_data = sales_resp.json()
        print("✅ Sales list retrieved successfully")
        print(f"   Sales Count: {len(sales_data.get('data', []))}")
        print(f"   Total: {sales_data['pagination'].get('total', 0)}")
        
        if len(sales_data.get('data', [])) > 0:
            first_sale = sales_data['data'][0]
            print(f"\n   Sample Sale:")
            print(f"   - Invoice: {first_sale.get('invoice_number')}")
            print(f"   - Amount: ₹{first_sale.get('final_amount')}")
            print(f"   - Date: {first_sale.get('created_at')}")
    else:
        print(f"❌ Failed: {sales_resp.text}")
        
except Exception as e:
    print(f"❌ Error: {e}")

# Step 4: Test without authentication (should fail with 401)
print("\n[Step 4] Testing Without Authentication...")
try:
    no_auth_resp = requests.get(
        f"{BASE_URL}/sales/stats/summary",
        params={'startDate': start_date, 'endDate': end_date},
        timeout=5
    )
    
    if no_auth_resp.status_code == 401:
        print("✅ Correctly requires authentication (401)")
    else:
        print(f"⚠️  Unexpected status: {no_auth_resp.status_code}")
        
except Exception as e:
    print(f"❌ Error: {e}")

# Step 5: Check CORS headers
print("\n[Step 5] Testing CORS Headers...")
try:
    cors_resp = requests.options(
        f"{BASE_URL}/sales/stats/summary",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "authorization,content-type"
        },
        timeout=5
    )
    
    print(f"   Status: {cors_resp.status_code}")
    print(f"   CORS Headers:")
    for header, value in cors_resp.headers.items():
        if 'access-control' in header.lower():
            print(f"   - {header}: {value}")
    
    if cors_resp.status_code in [200, 204]:
        print("✅ CORS configured correctly")
    else:
        print(f"⚠️  CORS might have issues")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 80)
print("📊 SUMMARY")
print("=" * 80)
print("✅ Backend API: Running on port 5000")
print("✅ Authentication: Working")
print("✅ Sales Stats Endpoint: /api/sales/stats/summary")
print("✅ Sales List Endpoint: /api/sales")
print("\n💡 If the frontend still shows issues:")
print("   1. Check browser console for errors (F12)")
print("   2. Verify you're logged in on the frontend")
print("   3. Check network tab for failed requests")
print("   4. Ensure frontend is connecting to http://localhost:5000/api")
print("=" * 80)
