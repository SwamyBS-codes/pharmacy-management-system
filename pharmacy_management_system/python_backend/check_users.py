#!/usr/bin/env python3
"""Check users in database"""

from db import execute_query

# Get all users
users = execute_query("SELECT id, email, name, role FROM users")

print("Users in database:")
print("=" * 60)
for user in users:
    print(f"ID: {user['id']}")
    print(f"  Email: {user['email']}")
    print(f"  Name: {user['name']}")
    print(f"  Role: {user['role']}")
    print()

if not users:
    print("No users found in database")
