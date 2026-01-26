"""Test the sales stats API endpoint"""
import requests
import json

BASE_URL = "http://localhost:5000/api"

print("=" * 70)
print("🧪 SALES STATS API TEST")
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
    
    # Test sales stats endpoint
    print("\n" + "=" * 70)
    print("Testing /api/sales/stats/summary")
    print("=" * 70)
    
    response = requests.get(
        f"{BASE_URL}/sales/stats/summary",
        headers=headers,
        timeout=10
    )
    
    print(f"\n📊 Response Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ SUCCESS! Response Body:")
        print(json.dumps(data, indent=2, default=str))
        
        print(f"\n📈 Summary Stats:")
        if 'summary' in data:
            print(f"   Total Sales: ₹{data['summary'].get('total_sales', 0)}")
            print(f"   Total Transactions: {data['summary'].get('total_transactions', 0)}")
            print(f"   Average Sale: ₹{data['summary'].get('avg_sale', 0)}")
        
        print(f"\n📅 Daily Sales: {len(data.get('dailySales', []))} days")
        if data.get('dailySales'):
            for day in data['dailySales'][:5]:
                print(f"   {day['date']}: ₹{day['sales']} ({day['transactions']} orders)")
        
        print(f"\n💊 Top Medicines: {len(data.get('topMedicines', []))} items")
        if data.get('topMedicines'):
            for med in data['topMedicines'][:5]:
                print(f"   {med['medicine_name']}: {med['total_quantity']} units (₹{med['total_revenue']})")
    else:
        print(f"\n❌ ERROR: {response.status_code}")
        print(response.json())
        
except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}: {e}")

print("\n" + "=" * 70)
