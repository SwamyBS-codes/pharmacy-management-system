"""Test the login API endpoint"""
import requests
import json

BASE_URL = "http://localhost:5000/api"

print("=" * 70)
print("🧪 LOGIN API TEST")
print("=" * 70)

# Test credentials
test_email = "swamybs272@gmail.com"
test_password = "Test@1234"

print(f"\n📝 Testing login with:")
print(f"   Email: {test_email}")
print(f"   Password: {test_password}")

try:
    # Make login request
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": test_email,
            "password": test_password
        },
        timeout=5
    )
    
    print(f"\n📊 Response Status: {response.status_code}")
    
    data = response.json()
    print(f"📊 Response Body:")
    print(json.dumps(data, indent=2))
    
    if response.status_code == 200:
        print("\n✅ LOGIN SUCCESSFUL!")
        
        if 'token' in data:
            print(f"   Token: {data['token'][:50]}...")
        if 'user' in data:
            print(f"   User: {data['user']['name']} ({data['user']['email']})")
            print(f"   Role: {data['user']['role']}")
            print(f"   Pharmacy: {data['user']['pharmacy_name']}")
    else:
        print(f"\n❌ LOGIN FAILED!")
        if 'error' in data:
            print(f"   Error: {data['error']}")
        if 'details' in data:
            print(f"   Details: {data['details']}")
            
except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}: {e}")

print("\n" + "=" * 70)

# Test with wrong password
print("\n🧪 TESTING WITH WRONG PASSWORD")
print("=" * 70)

print(f"\n📝 Testing login with:")
print(f"   Email: {test_email}")
print(f"   Password: WrongPassword123")

try:
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": test_email,
            "password": "WrongPassword123"
        },
        timeout=5
    )
    
    print(f"\n📊 Response Status: {response.status_code}")
    
    data = response.json()
    print(f"📊 Response Body:")
    print(json.dumps(data, indent=2))
    
    if response.status_code == 401:
        print("\n✅ CORRECTLY REJECTED WRONG PASSWORD")
    else:
        print(f"\n❌ UNEXPECTED RESPONSE")
        
except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}: {e}")

print("\n" + "=" * 70)

# Test with missing fields
print("\n🧪 TESTING WITH MISSING FIELDS")
print("=" * 70)

print(f"\n📝 Testing login with:")
print(f"   Email: {test_email}")
print(f"   Password: (empty)")

try:
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": test_email,
            "password": ""
        },
        timeout=5
    )
    
    print(f"\n📊 Response Status: {response.status_code}")
    
    data = response.json()
    print(f"📊 Response Body:")
    print(json.dumps(data, indent=2))
    
    if response.status_code == 400:
        print("\n✅ CORRECTLY REJECTED MISSING FIELDS")
    else:
        print(f"\n❌ UNEXPECTED RESPONSE")
        
except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}: {e}")

print("\n" + "=" * 70)
