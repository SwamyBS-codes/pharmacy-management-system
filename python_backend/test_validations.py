#!/usr/bin/env python3
"""
Test script for customer and user creation validations
Tests Indian mobile number validation and age (18+) validation
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000/api"

def test_customer_validations():
    """Test customer creation with various validation scenarios"""
    
    print("\n" + "="*70)
    print("TESTING CUSTOMER VALIDATIONS")
    print("="*70)
    
    # Test 1: Valid customer
    print("\n1. Valid Customer (Should succeed)")
    print("-" * 70)
    valid_customer = {
        "name": "Rajesh Kumar",
        "email": "rajesh@example.com",
        "phone": "9876543210",
        "address": "123 Main Street, Mumbai",
        "date_of_birth": "2000-01-15"
    }
    response = requests.post(f"{BASE_URL}/customers", json=valid_customer)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test 2: Invalid phone format (too short)
    print("\n2. Invalid Phone Format - Too Short (Should fail)")
    print("-" * 70)
    invalid_phone = {
        "name": "Priya Singh",
        "phone": "12345",
        "date_of_birth": "2000-05-20"
    }
    response = requests.post(f"{BASE_URL}/customers", json=invalid_phone)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test 3: Invalid phone (doesn't start with 6-9)
    print("\n3. Invalid Phone - Wrong Prefix (Should fail)")
    print("-" * 70)
    invalid_prefix = {
        "name": "Amit Patel",
        "phone": "5123456789",
        "date_of_birth": "1990-03-10"
    }
    response = requests.post(f"{BASE_URL}/customers", json=invalid_prefix)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test 4: Valid phone with +91 prefix
    print("\n4. Valid Phone with +91 Prefix (Should succeed)")
    print("-" * 70)
    valid_phone_prefix = {
        "name": "Neha Gupta",
        "phone": "+91-9812345678",
        "date_of_birth": "1995-07-22"
    }
    response = requests.post(f"{BASE_URL}/customers", json=valid_phone_prefix)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test 5: Age less than 18
    print("\n5. Age Less Than 18 (Should fail)")
    print("-" * 70)
    under_18 = {
        "name": "Aisha Khan",
        "phone": "8765432109",
        "date_of_birth": "2010-06-15"  # 13-14 years old
    }
    response = requests.post(f"{BASE_URL}/customers", json=under_18)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test 6: Future date of birth
    print("\n6. Future Date of Birth (Should fail)")
    print("-" * 70)
    future_dob = {
        "name": "Rahul Sharma",
        "phone": "9123456789",
        "date_of_birth": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    }
    response = requests.post(f"{BASE_URL}/customers", json=future_dob)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test 7: Exactly 18 years old (Should succeed)
    print("\n7. Exactly 18 Years Old (Should succeed)")
    print("-" * 70)
    age_18 = {
        "name": "Sneha Desai",
        "phone": "9987654321",
        "date_of_birth": (datetime.now() - timedelta(days=365*18 + 1)).strftime("%Y-%m-%d")
    }
    response = requests.post(f"{BASE_URL}/customers", json=age_18)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test 8: Invalid email format
    print("\n8. Invalid Email Format (Should fail)")
    print("-" * 70)
    invalid_email = {
        "name": "Vikram Rao",
        "phone": "9234567890",
        "email": "invalid-email",
        "date_of_birth": "1988-04-18"
    }
    response = requests.post(f"{BASE_URL}/customers", json=invalid_email)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    try:
        test_customer_validations()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to backend at", BASE_URL)
        print("Make sure the Flask server is running on port 5000")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
