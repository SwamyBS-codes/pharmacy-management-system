"""Test the sales stats API to see what it returns"""
import requests
import json

BASE_URL = "http://localhost:5000/api"
EMAIL = "swamybs272@gmail.com"
PASSWORD = "Test@1234"

print("=" * 80)
print("🧪 TEST SALES STATS API RESPONSE")
print("=" * 80)

# Login first
print("\n1. Logging in...")
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"email": EMAIL, "password": PASSWORD},
    timeout=5
)

if login_response.status_code != 200:
    print(f"❌ Login failed: {login_response.json()}")
    exit(1)

token = login_response.json()['token']
headers = {"Authorization": f"Bearer {token}"}
print("✅ Login successful")

# Get sales stats
print("\n2. Calling /api/sales/stats/summary...")
response = requests.get(
    f"{BASE_URL}/sales/stats/summary",
    headers=headers,
    timeout=10
)

print(f"\n📊 Response Status: {response.status_code}")
print(f"Response Headers: {dict(response.headers)}")

if response.status_code == 200:
    data = response.json()
    print("\n✅ SUCCESS! Response Body:")
    print(json.dumps(data, indent=2, default=str))
    
    print("\n📊 Analysis:")
    print(f"   - Summary keys: {list(data.get('summary', {}).keys())}")
    print(f"   - Daily sales count: {len(data.get('dailySales', []))}")
    print(f"   - Top medicines count: {len(data.get('topMedicines', []))}")
    
    if data.get('dailySales'):
        print(f"\n   First daily sale entry:")
        print(f"      {json.dumps(data['dailySales'][0], indent=8, default=str)}")
else:
    print(f"\n❌ ERROR Response:")
    print(json.dumps(response.json(), indent=2))

print("\n" + "=" * 80)
