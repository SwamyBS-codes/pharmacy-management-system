"""Test script to verify authentication works correctly"""
import bcrypt
import sys

def hash_password(password):
    """Hash a password using bcrypt with proper encoding"""
    if not password or not isinstance(password, str):
        raise ValueError("Password must be a non-empty string")
    
    # Encode password and hash it
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    # Return as string
    return hashed.decode('utf-8')

def verify_password(password, hashed_password):
    """Verify password against hash with robust error handling"""
    try:
        if not password or not hashed_password:
            print("❌ Empty password or hash provided")
            return False
        
        # Ensure both are strings
        if isinstance(password, bytes):
            password = password.decode('utf-8')
        if isinstance(hashed_password, bytes):
            hashed_password = hashed_password.decode('utf-8')
        
        # Clean inputs
        password = str(password).strip()
        hashed_password = str(hashed_password).strip()
        
        # Perform verification
        is_valid = bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        return is_valid
    except Exception as e:
        print(f"❌ Password verification error: {type(e).__name__}: {e}")
        return False

# Test cases
print("=" * 60)
print("🧪 PASSWORD AUTHENTICATION TESTS")
print("=" * 60)

test_password = "TestPassword123"
test_cases = [
    ("Test1234", "Test1234", True),
    ("Test1234", "WrongPassword", False),
    ("MyPassword2024", "MyPassword2024", True),
    ("Pharmacy@123", "Pharmacy@123", True),
]

all_passed = True

for pwd, verify_pwd, should_match in test_cases:
    print(f"\n📝 Test: password='{pwd}', verify='{verify_pwd}', should_match={should_match}")
    
    try:
        # Hash the password
        hashed = hash_password(pwd)
        print(f"   ✅ Password hashed: {hashed[:40]}...")
        
        # Verify the password
        is_valid = verify_password(verify_pwd, hashed)
        
        if is_valid == should_match:
            print(f"   ✅ Verification result: {is_valid} (expected {should_match})")
        else:
            print(f"   ❌ Verification result: {is_valid} (expected {should_match})")
            all_passed = False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        all_passed = False

print("\n" + "=" * 60)

# Test with existing hash
print("\n🔒 Testing with provided hash:")
provided_hash = "$2b$12$JYODybB8uYQyvFoe.IzxwOYnSUurMINz8i1RyNt0kfEDl7t.HyzM6"
test_pwd = "Test1234"

print(f"Hash: {provided_hash}")
print(f"Testing password: '{test_pwd}'")

is_valid = verify_password(test_pwd, provided_hash)
print(f"Result: {is_valid}")

if is_valid:
    print("✅ Hash verification successful!")
else:
    print("❌ Hash verification failed!")
    print("\nTrying to re-hash and verify...")
    try:
        new_hash = hash_password(test_pwd)
        new_result = verify_password(test_pwd, new_hash)
        print(f"New hash: {new_hash[:40]}...")
        print(f"New verification result: {new_result}")
        if new_result:
            print("✅ Fresh hash works correctly!")
    except Exception as e:
        print(f"❌ Error: {e}")

print("\n" + "=" * 60)
if all_passed:
    print("✅ ALL TESTS PASSED")
else:
    print("❌ SOME TESTS FAILED")
print("=" * 60)
