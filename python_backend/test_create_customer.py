"""Quick test to create a customer via API"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000/api"

print("=" * 70)
print("🧪 CREATE CUSTOMER API TEST")
print("=" * 70)

# Test credentials
email = "swamybs272@gmail.com"
password = "Test@1234"

try:
    # Login
    r = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password}, timeout=5)
    if r.status_code != 200:
        print("❌ Login failed:", r.status_code, r.text)
        raise SystemExit(1)
    token = r.json()['token']
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    print("✅ Logged in")

    # Create a new customer payload
    payload = {
        "name": "Test Customer",
        "email": f"test.customer.{int(datetime.now().timestamp())}@example.com",
        "phone": "9876543210",
        "address": "123 Test Street, City",
        "date_of_birth": "1990-05-15"
    }

    print("\n➡️  Creating customer with payload:")
    print(json.dumps(payload, indent=2))

    resp = requests.post(f"{BASE_URL}/customers", headers=headers, json=payload, timeout=10)
    print("\n📊 Response Status:", resp.status_code)

    try:
        data = resp.json()
        print("📦 Response Body:")
        print(json.dumps(data, indent=2, default=str))
    except Exception:
        print("Raw:", resp.text)

    if resp.status_code == 201:
        print("\n✅ Customer created successfully!")
    else:
        print("\n❌ Failed to create customer")

except Exception as e:
    print("\n❌ ERROR:", type(e).__name__, e)

print("\n" + "=" * 70)
