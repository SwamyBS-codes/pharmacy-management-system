"""
Script to check and verify password for user
"""
import bcrypt
from db import execute_query
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_user_password():
    """Check what password hash exists for the user"""
    
    email = "swamybs272@gmail.com"
    
    # Get user from database
    query = """
        SELECT id, name, email, password, role, is_active
        FROM users
        WHERE LOWER(TRIM(email)) = %s
    """
    
    user = execute_query(query, (email.lower(),), fetch_one=True)
    
    if not user:
        print(f"❌ No user found with email: {email}")
        return
    
    print(f"\n✅ User found:")
    print(f"   ID: {user['id']}")
    print(f"   Name: {user['name']}")
    print(f"   Email: {user['email']}")
    print(f"   Role: {user['role']}")
    print(f"   Active: {user['is_active']}")
    print(f"   Password Hash: {user['password'][:50]}...")
    
    # Test various common passwords
    test_passwords = [
        'admin123',
        'Admin123',
        'password',
        'admin',
        'admin@123',
        '12345678',
    ]
    
    print(f"\n🔍 Testing common passwords:")
    for pwd in test_passwords:
        try:
            is_valid = bcrypt.checkpw(pwd.encode('utf-8'), user['password'].encode('utf-8'))
            if is_valid:
                print(f"   ✅ '{pwd}' - MATCH!")
            else:
                print(f"   ❌ '{pwd}' - no match")
        except Exception as e:
            print(f"   ❌ '{pwd}' - error: {e}")
    
    # Allow user to test custom password
    print(f"\n💡 To test a specific password, enter it below (or press Enter to skip):")
    custom_pwd = input("Password: ").strip()
    
    if custom_pwd:
        try:
            is_valid = bcrypt.checkpw(custom_pwd.encode('utf-8'), user['password'].encode('utf-8'))
            if is_valid:
                print(f"   ✅ Password '{custom_pwd}' is CORRECT!")
            else:
                print(f"   ❌ Password '{custom_pwd}' is incorrect")
        except Exception as e:
            print(f"   ❌ Error testing password: {e}")
    
    # Offer to reset password
    print(f"\n💡 Want to reset the password? (y/n):")
    reset = input().strip().lower()
    
    if reset == 'y':
        new_password = input("Enter new password (min 8 chars): ").strip()
        if len(new_password) >= 8:
            # Hash new password
            salt = bcrypt.gensalt(rounds=12)
            hashed = bcrypt.hashpw(new_password.encode('utf-8'), salt)
            
            # Update in database
            update_query = """
                UPDATE users
                SET password = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """
            execute_query(update_query, (hashed.decode('utf-8'), user['id']), fetch_all=False)
            print(f"\n✅ Password updated successfully!")
            print(f"   Email: {email}")
            print(f"   New Password: {new_password}")
        else:
            print("❌ Password must be at least 8 characters")

if __name__ == "__main__":
    check_user_password()
