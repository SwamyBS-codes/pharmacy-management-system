"""Script to reset the test user's password"""
from db import execute_query
import bcrypt
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def hash_password(password):
    """Hash a password using bcrypt with proper encoding"""
    if not password or not isinstance(password, str):
        raise ValueError("Password must be a non-empty string")
    
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

print("=" * 60)
print("🔐 ADMIN PASSWORD RESET")
print("=" * 60)

# Test password
test_password = "Test@1234"

try:
    # Hash the new password
    hashed = hash_password(test_password)
    print(f"\n✅ Password hashed successfully")
    print(f"   Hash: {hashed[:50]}...")
    
    # Update the admin user's password
    query = """
        UPDATE users
        SET password = %s, updated_at = CURRENT_TIMESTAMP
        WHERE email = 'swamybs272@gmail.com'
        RETURNING id, name, email, role
    """
    
    result = execute_query(query, (hashed,), fetch_one=True)
    
    if result:
        print(f"\n✅ Admin password reset successfully")
        print(f"   User ID: {result['id']}")
        print(f"   Name: {result['name']}")
        print(f"   Email: {result['email']}")
        print(f"   Role: {result['role']}")
        print(f"\n📝 Test credentials:")
        print(f"   Email: {result['email']}")
        print(f"   Password: {test_password}")
    else:
        print("\n❌ Failed to update password")
        
except Exception as e:
    logger.error(f"Error: {type(e).__name__}: {e}")
    print(f"\n❌ Error: {e}")

print("\n" + "=" * 60)
