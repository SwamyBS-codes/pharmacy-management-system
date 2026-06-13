"""
Test script to verify authentication is working correctly
Run this script to test the authentication endpoints
"""

import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_login():
    """Test login endpoint"""
    print("\n" + "="*50)
    print("Testing Login Endpoint")
    print("="*50)
    
    # Test with existing user
    login_data = {
        "email": "swamybs272@gmail.com",
        "password": "admin123"  # Update with actual password
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login successful!")
            print(f"User: {data.get('user', {}).get('name')}")
            print(f"Email: {data.get('user', {}).get('email')}")
            print(f"Role: {data.get('user', {}).get('role')}")
            print(f"Token: {data.get('token', '')[:20]}...")
            return data.get('token')
        else:
            print(f"❌ Login failed: {response.json()}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_get_current_user(token):
    """Test /me endpoint to verify token"""
    print("\n" + "="*50)
    print("Testing Get Current User Endpoint")
    print("="*50)
    
    try:
        response = requests.get(
            f"{BASE_URL}/auth/me",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Token validation successful!")
            print(f"User: {data.get('name')}")
            print(f"Email: {data.get('email')}")
            print(f"Role: {data.get('role')}")
        else:
            print(f"❌ Token validation failed: {response.json()}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_logout(token):
    """Test logout endpoint"""
    print("\n" + "="*50)
    print("Testing Logout Endpoint")
    print("="*50)
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/logout",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Logout successful!")
        else:
            print(f"❌ Logout failed: {response.json()}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_email_case_sensitivity():
    """Test login with different email cases"""
    print("\n" + "="*50)
    print("Testing Email Case Sensitivity")
    print("="*50)
    
    test_cases = [
        "swamybs272@gmail.com",
        "SWAMYBS272@GMAIL.COM",
        "SwAmYbS272@GmAiL.cOm",
    ]
    
    for email in test_cases:
        print(f"\nTrying with email: {email}")
        login_data = {
            "email": email,
            "password": "admin123"  # Update with actual password
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/auth/login",
                json=login_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                print(f"  ✅ Success (normalized to lowercase)")
            else:
                print(f"  ❌ Failed: {response.json().get('error')}")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")

def main():
    """Run all tests"""
    print("\n" + "="*70)
    print(" AUTHENTICATION SYSTEM TEST")
    print("="*70)
    
    # Test 1: Login
    token = test_login()
    
    if token:
        # Test 2: Verify token
        test_get_current_user(token)
        
        # Test 3: Logout
        test_logout(token)
    
    # Test 4: Email case sensitivity
    test_email_case_sensitivity()
    
    print("\n" + "="*70)
    print(" TESTS COMPLETED")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
