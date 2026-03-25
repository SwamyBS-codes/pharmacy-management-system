#!/usr/bin/env python3
"""
Test script to debug registration and login issue
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000/api"

def test_existing_user_login():
    """Test login with known admin credentials"""
    
    test_email = "swamybs272@gmail.com"  # Use existing admin
    test_password = "Swamybs@12345"
    
    print("\n" + "="*70)
    print("TESTING LOGIN WITH EXISTING USER")
    print("="*70)
    
    # Test 1: Login with credentials
    print(f"\n1. LOGIN WITH CREDENTIALS")
    print("-" * 70)
    print(f"Email: {test_email}")
    print(f"Password: {test_password}")
    
    login_data = {
        "email": test_email,
        "password": test_password,
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"\nStatus: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Login successful")
        print(f"   User: {result['user']['name']}")
        print(f"   Email: {result['user']['email']}")
        print(f"   Token: {result['token'][:20]}...")
        return True
    else:
        print(f"❌ Login failed")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return False
    
def test_login_variations(email, password):
    """Test various login scenarios"""
    print(f"\n2. LOGIN WITH UPPERCASE EMAIL")
    print("-" * 70)
    uppercase_email = email.upper()
    print(f"Email: {uppercase_email}")
    
    login_data = {
        "email": uppercase_email,
        "password": password,
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        print(f"✅ Login with uppercase email successful")
    else:
        print(f"❌ Login with uppercase email failed")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test 3: Try login with wrong password
    print(f"\n3. LOGIN WITH WRONG PASSWORD")
    print("-" * 70)
    print(f"Email: {email}")
    print(f"Password: WrongPassword123")
    
    login_data = {
        "email": email,
        "password": "WrongPassword123",
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        print(f"❌ Login should have failed but succeeded!")
    else:
        print(f"✅ Login correctly rejected")
        print(f"Error: {response.json()['error']}")
    
    # Test 4: Try login with extra spaces
    print(f"\n4. LOGIN WITH SPACES AROUND EMAIL")
    print("-" * 70)
    spaced_email = f"  {email}  "
    print(f"Email: '{spaced_email}'")
    
    login_data = {
        "email": spaced_email,
        "password": password,
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        print(f"✅ Login with spaces handled correctly")
    else:
        print(f"❌ Login failed")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    try:
        success = test_existing_user_login()
        if success:
            test_login_variations("swamybs272@gmail.com", "Swamybs@12345")
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to backend at", BASE_URL)
        print("Make sure the Flask server is running on port 5000")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
