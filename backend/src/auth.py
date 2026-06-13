"""
Authentication API Routes
Handles user registration, login, logout, and profile management
"""
from flask import Blueprint, request, jsonify
from db import execute_query
import bcrypt
import jwt
import logging
from datetime import datetime, timedelta
from config import Config
from middleware import require_auth, require_role

logger = logging.getLogger(__name__)
auth_bp = Blueprint('auth', __name__)

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
            logger.warning("Empty password or hash provided")
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
        logger.debug(f"Password verification result: {is_valid}")
        return is_valid
    except Exception as e:
        logger.error(f"Password verification error: {type(e).__name__}: {e}")
        return False

def generate_token(user_id, pharmacy_id):
    """Generate JWT token for user"""
    expires_at = datetime.now() + timedelta(hours=24)
    
    payload = {
        'user_id': user_id,
        'pharmacy_id': pharmacy_id,
        'exp': expires_at
    }
    
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
    
    # Store token in database if possible; allow login to succeed even if token storage is unavailable
    token_query = """
        INSERT INTO auth_tokens (user_id, token, expires_at)
        VALUES (%s, %s, %s)
        RETURNING id
    """
    try:
        execute_query(token_query, (user_id, token, expires_at), fetch_one=True)
    except Exception as e:
        logger.warning(f"Unable to store auth token in auth_tokens table: {e}")
    
    return token

@auth_bp.route('/admin-reset', methods=['POST'])
def admin_reset_password():
    """Securely reset the ADMIN user's password (development-only).
    Requires `ADMIN_SETUP_KEY` in env and DEBUG enabled.
    Body: { email, new_password, setup_key }
    """
    try:
        data = request.get_json() or {}

        # Guardrails: only allow in debug/dev mode
        if not Config.DEBUG:
            return jsonify({'error': 'Not allowed in production'}), 403

        setup_key = data.get('setup_key')
        if not Config.ADMIN_SETUP_KEY:
            return jsonify({'error': 'Setup key not configured'}), 400
        if not setup_key or setup_key != Config.ADMIN_SETUP_KEY:
            return jsonify({'error': 'Invalid setup key'}), 403

        email = data.get('email')
        new_password = data.get('new_password')
        if not email or not new_password:
            return jsonify({'error': 'Email and new_password are required'}), 400

        # Find admin user by email
        user_row = execute_query(
            """
            SELECT id, role FROM users
            WHERE email = %s AND role = 'ADMIN'
            """,
            (email,),
            fetch_one=True
        )

        if not user_row:
            return jsonify({'error': 'Admin user not found for provided email'}), 404

        # Update password
        hashed = hash_password(new_password)
        execute_query(
            """
            UPDATE users
            SET password = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
            """,
            (hashed, user_row['id']),
            fetch_all=False
        )

        return jsonify({'message': 'Admin password reset successfully'}), 200
    except Exception as e:
        logger.error(f"Error resetting admin password: {e}")
        return jsonify({'error': 'Failed to reset password', 'details': str(e)}), 500

@auth_bp.route('/check-pharmacy', methods=['GET'])
def check_pharmacy():
    """Check if a pharmacy is already registered"""
    try:
        query = "SELECT COUNT(*) as count FROM pharmacy"
        result = execute_query(query, fetch_one=True)
        
        return jsonify({
            'exists': result['count'] > 0,
            'count': result['count']
        }), 200
    except Exception as e:
        logger.error(f"Error checking pharmacy: {e}")
        return jsonify({'error': 'Failed to check pharmacy registration'}), 500

@auth_bp.route('/register-pharmacy', methods=['POST'])
def register_pharmacy():
    """Register a new pharmacy and admin user"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        # Extract and validate input
        pharmacy_name = data.get('pharmacy_name', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '').strip()
        
        logger.info(f"Registration attempt for pharmacy: {pharmacy_name}, email: {email}")
        
        # Validate required fields
        if not pharmacy_name or not email or not password:
            logger.warning("Registration failed: Missing required fields")
            return jsonify({'error': 'Pharmacy name, email, and password are required'}), 400
        
        # Validate email format
        if '@' not in email or '.' not in email:
            return jsonify({'error': 'Please enter a valid email address'}), 400
        
        # Validate password length
        if len(password) < 8:
            return jsonify({'error': 'Password must be at least 8 characters'}), 400
        
        # Check if pharmacy already exists
        pharmacy_count = execute_query("SELECT COUNT(*) as count FROM pharmacy", fetch_one=True)
        
        if pharmacy_count['count'] > 0:
            logger.warning("Registration rejected: Pharmacy already registered")
            return jsonify({'error': 'A pharmacy is already registered. Only one pharmacy allowed.'}), 409
        
        # Check if email already exists
        email_count = execute_query(
            "SELECT COUNT(*) as count FROM users WHERE LOWER(TRIM(email)) = %s",
            (email,),
            fetch_one=True
        )
        
        if email_count['count'] > 0:
            logger.warning(f"Registration failed: Email already exists: {email}")
            return jsonify({'error': 'Email already registered'}), 409
        
        # Hash password
        try:
            hashed_password = hash_password(password)
            logger.debug(f"Password hashed successfully for {email}")
        except Exception as e:
            logger.error(f"Failed to hash password: {e}")
            return jsonify({'error': 'Failed to process password'}), 500
        
        # Create pharmacy
        pharmacy_result = execute_query(
            """
            INSERT INTO pharmacy (pharmacy_name, email, is_profile_complete)
            VALUES (%s, %s, FALSE)
            RETURNING id, pharmacy_name, email, is_profile_complete
            """,
            (pharmacy_name, email),
            fetch_one=True
        )
        
        if not pharmacy_result:
            logger.error("Failed to create pharmacy record")
            return jsonify({'error': 'Failed to create pharmacy'}), 500
        
        pharmacy_id = pharmacy_result['id']
        logger.info(f"Pharmacy created with ID: {pharmacy_id}")
        
        # Create admin user
        user_result = execute_query(
            """
            INSERT INTO users (pharmacy_id, name, email, password, role, status, is_active)
            VALUES (%s, %s, %s, %s, %s, 'active', TRUE)
            RETURNING id, name, email, role
            """,
            (pharmacy_id, 'Admin', email, hashed_password, 'ADMIN'),
            fetch_one=True
        )
        
        if not user_result:
            logger.error("Failed to create user record")
            return jsonify({'error': 'Failed to create user'}), 500
        
        logger.info(f"User created with ID: {user_result['id']}")
        
        # Generate token
        token = generate_token(user_result['id'], pharmacy_id)
        logger.info(f"Token generated for new user: {email}")
        
        return jsonify({
            'success': True,
            'message': 'Registration successful',
            'pharmacy': pharmacy_result,
            'user': {
                'id': user_result['id'],
                'name': user_result['name'],
                'email': user_result['email'],
                'role': user_result['role'],
                'pharmacy_id': pharmacy_id,
                'pharmacy_name': pharmacy_result['pharmacy_name'],
                'is_profile_complete': pharmacy_result['is_profile_complete']
            },
            'token': token
        }), 201
        
    except Exception as e:
        logger.error(f"Unexpected error during registration: {type(e).__name__}: {e}", exc_info=True)
        if 'duplicate' in str(e).lower() or 'unique' in str(e).lower():
            return jsonify({'error': 'Email already exists'}), 409
        return jsonify({
            'error': 'Registration failed. Please try again.',
            'details': str(e) if Config.DEBUG else None
        }), 500

@auth_bp.route('/complete-profile', methods=['POST'])
@require_auth
def complete_profile():
    """Complete pharmacy profile with additional details"""
    try:
        data = request.get_json()
        user = request.current_user
        
        # Validate required fields
        if not data.get('address') or not data.get('phone'):
            return jsonify({'error': 'Address and phone are required'}), 400
        
        # Update pharmacy profile
        update_query = """
            UPDATE pharmacy
            SET address = %s,
                phone = %s,
                license_number = %s,
                gst_number = %s,
                is_profile_complete = TRUE,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
            RETURNING id, pharmacy_name, address, phone, license_number, gst_number, email, is_profile_complete
        """
        pharmacy = execute_query(
            update_query,
            (
                data['address'],
                data['phone'],
                data.get('license_number'),
                data.get('gst_number'),
                user['pharmacy_id']
            ),
            fetch_one=True
        )
        
        return jsonify({
            'message': 'Pharmacy profile completed successfully',
            'pharmacy': pharmacy
        }), 200
        
    except Exception as e:
        logger.error(f"Error completing profile: {e}")
        return jsonify({'error': 'Failed to complete profile', 'details': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and return JWT token"""
    try:
        data = request.get_json()
        
        # Validate input
        if not data:
            logger.warning("Login attempt with empty request body")
            return jsonify({'error': 'Request body is required'}), 400
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email or not password:
            logger.warning(f"Login attempt with missing fields - email: {bool(email)}, password: {bool(password)}")
            return jsonify({'error': 'Email and password are required'}), 400
        
        logger.info(f"Login attempt for: {email}")
        
        # Find user by email
        user_query = """
            SELECT u.id, u.name, u.email, u.password, u.role, u.pharmacy_id, u.is_active,
                   p.pharmacy_name, p.is_profile_complete
            FROM users u
            LEFT JOIN pharmacy p ON u.pharmacy_id = p.id
            WHERE LOWER(TRIM(u.email)) = %s
        """
        
        user = execute_query(user_query, (email,), fetch_one=True)
        
        if not user:
            logger.warning(f"No user found with email: {email}")
            return jsonify({'error': 'Invalid email or password'}), 401
        
        logger.debug(f"User found: {user['email']} (ID: {user['id']}), Active: {user['is_active']}")
        
        # Check if user is active
        if not user['is_active']:
            logger.warning(f"Login attempt for inactive account: {email}")
            return jsonify({'error': 'Account is deactivated. Please contact administrator.'}), 403
        
        # Verify password
        password_valid = verify_password(password, user['password'])
        
        if not password_valid:
            logger.warning(f"Password verification failed for: {email}")
            return jsonify({'error': 'Invalid email or password'}), 401
        
        logger.info(f"Password verified successfully for: {email}")
        
        # Generate token
        token = generate_token(user['id'], user['pharmacy_id'])
        logger.info(f"Token generated for user: {email} (ID: {user['id']})")
        
        # Prepare user data for response
        user_data = {
            'id': user['id'],
            'name': user['name'],
            'email': user['email'],
            'role': user['role'],
            'pharmacy_id': user['pharmacy_id'],
            'pharmacy_name': user['pharmacy_name'],
            'is_profile_complete': user['is_profile_complete']
        }
        
        logger.info(f"Successful login for: {email}")
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': user_data,
            'token': token
        }), 200
        
    except Exception as e:
        logger.error(f"Unexpected error during login: {type(e).__name__}: {e}", exc_info=True)
        return jsonify({
            'error': 'Login failed. Please try again.',
            'details': str(e) if Config.DEBUG else None
        }), 500

@auth_bp.route('/logout', methods=['POST'])
@require_auth
def logout():
    """Logout user and invalidate token"""
    try:
        from middleware import get_token_from_header
        token = get_token_from_header()
        
        if token:
            # Invalidate token
            execute_query(
                "UPDATE auth_tokens SET is_valid = FALSE WHERE token = %s",
                (token,),
                fetch_all=False
            )
        
        return jsonify({'message': 'Logout successful'}), 200
        
    except Exception as e:
        logger.error(f"Error during logout: {e}")
        return jsonify({'error': 'Logout failed'}), 500

@auth_bp.route('/me', methods=['GET'])
@require_auth
def get_current_user():
    """Get current user profile"""
    try:
        user = request.current_user
        
        return jsonify({
            'id': user['id'],
            'name': user['name'],
            'email': user['email'],
            'role': user['role'],
            'pharmacy_id': user['pharmacy_id'],
            'pharmacy_name': user['pharmacy_name']
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting current user: {e}")
        return jsonify({'error': 'Failed to get user profile'}), 500

@auth_bp.route('/change-password', methods=['POST'])
@require_auth
def change_password():
    """Change user password"""
    try:
        data = request.get_json()
        user = request.current_user
        
        # Validate required fields
        if not data.get('current_password') or not data.get('new_password'):
            return jsonify({'error': 'Current password and new password are required'}), 400
        
        # Get user's current password
        password_query = "SELECT password FROM users WHERE id = %s"
        result = execute_query(password_query, (user['id'],), fetch_one=True)
        
        # Verify current password
        if not verify_password(data['current_password'], result['password']):
            return jsonify({'error': 'Current password is incorrect'}), 401
        
        # Validate new password
        if len(data['new_password']) < 8:
            return jsonify({'error': 'New password must be at least 8 characters'}), 400
        
        # Hash new password
        hashed_password = hash_password(data['new_password'])
        
        # Update password
        update_query = """
            UPDATE users
            SET password = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        execute_query(update_query, (hashed_password, user['id']), fetch_all=False)
        
        return jsonify({'message': 'Password changed successfully'}), 200
        
    except Exception as e:
        logger.error(f"Error changing password: {e}")
        return jsonify({'error': 'Failed to change password'}), 500
