#!/usr/bin/env python3
"""Check password hashes in database"""

from db import execute_query
import bcrypt

# Get users with password hashes
result = execute_query("""
    SELECT id, email, name, password 
    FROM users 
    WHERE email IN ('vinayak123@gmail.com', 'swamybs272@gmail.com')
""")

print("Users and their password hashes:")
print("=" * 80)

for user in result:
    email = user['email']
    password_hash = user['password']
    
    print(f"\nUser: {email}")
    print(f"Hash: {password_hash[:20]}...{password_hash[-10:]}")
    print(f"\nTesting passwords:")
    
    # Test various passwords
    test_passwords = [
        "vinayak@123",
        "Vinayak@123",
        "vinayak123",
        "Vinayak123",
        "swamybs@12345",
        "Swamybs@12345",
    ]
    
    for pwd in test_passwords:
        try:
            is_valid = bcrypt.checkpw(pwd.encode('utf-8'), password_hash.encode('utf-8'))
            status = "✅ MATCH" if is_valid else "❌ no match"
            print(f"  '{pwd}' → {status}")
        except Exception as e:
            print(f"  '{pwd}' → Error: {e}")
