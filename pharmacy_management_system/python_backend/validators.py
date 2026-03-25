"""
Validation utilities for form inputs
Includes Indian mobile number and age validation
"""
import re
from datetime import datetime, date

def validate_indian_mobile(phone: str) -> tuple[bool, str]:
    """
    Validate if phone number is a valid Indian mobile number
    
    Returns:
        tuple: (is_valid: bool, error_message: str)
    """
    if not phone:
        return False, "Phone number is required"
    
    # Remove all spaces and special characters except digits and +
    cleaned = re.sub(r'[^\d+]', '', phone)
    
    # Check if it starts with +91 or 91 or 0
    if cleaned.startswith('+91'):
        cleaned = cleaned[3:]
    elif cleaned.startswith('91'):
        cleaned = cleaned[2:]
    elif cleaned.startswith('0'):
        cleaned = cleaned[1:]
    
    # Valid Indian mobile should be exactly 10 digits
    if not re.match(r'^\d{10}$', cleaned):
        return False, "Invalid phone number format. Indian mobile numbers should be 10 digits"
    
    # Check if it's a valid mobile number prefix (6-9 for mobile)
    if not cleaned[0] in ['6', '7', '8', '9']:
        return False, "Invalid phone number. Mobile numbers should start with 6, 7, 8, or 9"
    
    return True, ""

def validate_age_18_plus(dob_str: str) -> tuple[bool, str]:
    """
    Validate if date of birth indicates person is 18+ years old
    
    Args:
        dob_str: Date of birth in 'YYYY-MM-DD' format or None
        
    Returns:
        tuple: (is_valid: bool, error_message: str)
    """
    if not dob_str:
        return False, "Date of birth is required"
    
    try:
        # Parse the date
        dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return False, "Invalid date format. Please use YYYY-MM-DD format"
    
    # Check if date is in the future
    if dob > date.today():
        return False, "Date of birth cannot be in the future"
    
    # Calculate age
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    
    # Check if age is at least 18
    if age < 18:
        return False, f"User must be at least 18 years old (Currently {age} years old)"
    
    return True, ""

def validate_customer_data(data: dict) -> tuple[bool, str]:
    """
    Validate customer data for creation/update
    
    Args:
        data: Dictionary containing customer fields
        
    Returns:
        tuple: (is_valid: bool, error_message: str)
    """
    # Name is required
    if not data.get('name'):
        return False, "Customer name is required"
    
    # Validate phone if provided
    if data.get('phone'):
        is_valid, error = validate_indian_mobile(data['phone'])
        if not is_valid:
            return False, error
    
    # Validate DOB if provided
    if data.get('date_of_birth'):
        is_valid, error = validate_age_18_plus(data['date_of_birth'])
        if not is_valid:
            return False, error
    
    # Validate email format if provided
    if data.get('email'):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', data['email']):
            return False, "Invalid email format"
    
    return True, ""

def validate_user_data(data: dict) -> tuple[bool, str]:
    """
    Validate user data for creation/update
    
    Args:
        data: Dictionary containing user fields
        
    Returns:
        tuple: (is_valid: bool, error_message: str)
    """
    # Name and email are required
    if not data.get('name'):
        return False, "Name is required"
    
    if not data.get('email'):
        return False, "Email is required"
    
    # Validate email format
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', data['email']):
        return False, "Invalid email format"
    
    # Password validation for creation (POST)
    if 'password' in data:
        if not data['password']:
            return False, "Password is required"
        if len(data['password']) < 8:
            return False, "Password must be at least 8 characters"
    
    # Validate phone if provided (for staff members)
    if data.get('phone'):
        is_valid, error = validate_indian_mobile(data['phone'])
        if not is_valid:
            return False, error
    
    # Validate DOB if provided
    if data.get('date_of_birth'):
        is_valid, error = validate_age_18_plus(data['date_of_birth'])
        if not is_valid:
            return False, error
    
    return True, ""
