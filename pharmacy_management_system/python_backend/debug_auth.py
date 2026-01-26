"""Debug script to check auth and user data"""
from db import execute_query
import bcrypt

# Check all users in database
print("=" * 60)
print("DEBUG: All Users in Database")
print("=" * 60)

users_query = """
    SELECT u.id, u.name, u.email, u.password, u.role, u.pharmacy_id, u.is_active,
           p.pharmacy_name
    FROM users u
    LEFT JOIN pharmacy p ON u.pharmacy_id = p.id
"""

users = execute_query(users_query, fetch_all=True)

if users:
    for user in users:
        print(f"\nUser ID: {user['id']}")
        print(f"  Name: {user['name']}")
        print(f"  Email: {user['email']}")
        print(f"  Email (repr): {repr(user['email'])}")
        print(f"  Email length: {len(user['email'])}")
        print(f"  Password hash: {user['password'][:30]}...")
        print(f"  Role: {user['role']}")
        print(f"  Pharmacy ID: {user['pharmacy_id']}")
        print(f"  Pharmacy Name: {user['pharmacy_name']}")
        print(f"  Is Active: {user['is_active']}")
else:
    print("No users found in database!")

# Check all pharmacies
print("\n" + "=" * 60)
print("DEBUG: All Pharmacies in Database")
print("=" * 60)

pharmacy_query = "SELECT id, pharmacy_name, email FROM pharmacy"
pharmacies = execute_query(pharmacy_query, fetch_all=True)

if pharmacies:
    for pharmacy in pharmacies:
        print(f"\nPharmacy ID: {pharmacy['id']}")
        print(f"  Name: {pharmacy['pharmacy_name']}")
        print(f"  Email: {pharmacy['email']}")
        print(f"  Email (repr): {repr(pharmacy['email'])}")
        print(f"  Email length: {len(pharmacy['email'])}")
else:
    print("No pharmacies found in database!")

# Test password verification
print("\n" + "=" * 60)
print("DEBUG: Test Password Verification")
print("=" * 60)

if users:
    test_user = users[0]
    test_password = "Test@1234"  # Change this to test
    
    print(f"\nTesting password for user: {test_user['email']}")
    print(f"Test password: {test_password}")
    print(f"Stored hash: {test_user['password'][:50]}...")
    
    try:
        result = bcrypt.checkpw(test_password.encode('utf-8'), test_user['password'].encode('utf-8'))
        print(f"Password matches: {result}")
        if result:
            print("✅ Password verification successful!")
        else:
            print("❌ Password verification failed!")
    except Exception as e:
        print(f"❌ Error during password verification: {e}")
