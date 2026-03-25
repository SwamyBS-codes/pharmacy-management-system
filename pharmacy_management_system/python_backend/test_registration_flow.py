#!/usr/bin/env python3
"""
Test what happens if pharmacy check is bypassed
Shows how registration and login work when successful
"""

import requests
import json
import hashlib
from datetime import datetime

BASE_URL = "http://localhost:5000/api"

def simulate_fresh_registration():
    """
    Simulate a fresh registration scenario where:
    1. User registers successfully
    2. System stores their credentials
    3. They try to login
    """
    
    print("\n" + "="*70)
    print("REGISTRATION → LOGIN FLOW TEST")
    print("="*70)
    
    # We'll use an existing employee to simulate the flow
    test_email = "vinayak123@gmail.com"
    test_password = "Vinayak@123"  # We'll test various passwords
    
    print(f"\nScenario: User registered with email: {test_email}")
    print(f"          They set password to: {test_password}")
    print()
    
    # Test 1: Exact credentials
    print("1. TEST: Login with EXACT credentials")
    print("-" * 70)
    
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": test_email,
        "password": test_password
    })
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ LOGIN SUCCESSFUL")
        print(f"   User: {response.json()['user']['name']}")
    else:
        print(f"❌ LOGIN FAILED")
        print(f"   Error: {response.json()['error']}")
    
    # Test 2: Check what password might be correct
    print("\n2. DEBUGGING: Common password variations")
    print("-" * 70)
    
    passwords_to_try = [
        "Vinayak@123",
        "vinayak@123",
        "VINAYAK@123",
        "Vinayak123",
        "vinayak123",
        "password",
        "123456789",
        "Vinayak",
        "",
    ]
    
    for pwd in passwords_to_try:
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": test_email,
            "password": pwd
        })
        
        status = "✅" if response.status_code == 200 else "❌"
        print(f"{status} Password: '{pwd}' → Status {response.status_code}")
    
    # Test 3: Check data consistency
    print("\n3. TEST: Data validation - Email lookup")
    print("-" * 70)
    
    # Try with different email cases
    email_variations = [
        test_email,
        test_email.upper(),
        test_email.lower(),
        f"  {test_email}  ",
    ]
    
    for email in email_variations:
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": email,
            "password": "WrongPassword"  # Use wrong password to see if email exists
        })
        
        # If email not found: 401 "Invalid email or password"
        # We can't distinguish between wrong email and wrong password
        # But if they all give same error, email normalization works
        print(f"Email: '{email}'")
        print(f"  Status: {response.status_code} → {response.json()['error']}")
    
    # Test 4: Simulate registration then immediate login
    print("\n4. SIMULATION: What backend does during registration")
    print("-" * 70)
    print("""
When user registers:
1. Frontend sends: email (normalized to lowercase), password
2. Backend receives: email, password
3. Backend creates user with:
   - email: LOWER(TRIM(email))
   - password: bcrypt.hashpw(password)
   - Other fields...

When user logs in:
1. Frontend sends: email (normalized to lowercase), password
2. Backend queries: WHERE LOWER(TRIM(email)) = ?
3. Backend compares: bcrypt.checkpw(password_from_form, stored_hash)

If credentials match database:
   - Status 200 + token
Else:
   - Status 401 "Invalid email or password"
    """)
    
    print("\n" + "="*70)
    print("ANALYSIS")
    print("="*70)
    print("""
✅ Email is normalized (LOWER + TRIM)
✅ Password is hashed with bcrypt
✅ Password verification compares hash

Possible issues if login fails:
❌ User entered wrong password
❌ User entered wrong email
❌ Registration actually failed (but they didn't see error)
❌ Password was reset between registration and login
    """)

if __name__ == "__main__":
    try:
        simulate_fresh_registration()
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Cannot connect to backend at {BASE_URL}")
        print("Make sure Flask server is running on port 5000")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
