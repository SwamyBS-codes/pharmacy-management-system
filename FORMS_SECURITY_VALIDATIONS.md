# Forms, Security & Validations Design

## Table of Contents
1. [Form Design](#form-design)
2. [Security Architecture](#security-architecture)
3. [Validation Strategy](#validation-strategy)

---

## Form Design

### 1. **Client-Side Form Implementation**

#### Form Framework
- **React + React Router**: Component-based forms with TypeScript
- **State Management**: React hooks (`useState`, `useContext`)
- **Form Handling**: Direct state management with controlled components
- **Styling**: Tailwind CSS with custom styling

#### Key Form Components

##### **Authentication Forms**

**Login Form** ([client/pages/Login.tsx](client/pages/Login.tsx))
```tsx
- Email input with format validation
- Password input with show/hide toggle
- Error message display
- Loading state management
- Form submission handling with API integration
```

**Signup Form** ([client/pages/Signup.tsx](client/pages/Signup.tsx))
```tsx
- Pharmacy name input
- Email validation with regex: /^[^\s@]+@[^\s@]+\.[^\s@]+$/
- Password with confirmation
- Password requirements indicator:
  * At least 8 characters
  * Uppercase letter
  * Lowercase letter
  * Number
- Real-time validation feedback
```

**Profile Completion Form**
```tsx
- Address input
- Phone number
- License number (optional)
- GST number (optional)
- Multi-step form with back/next navigation
```

##### **User Management Forms** ([client/pages/dashboard/Users.tsx](client/pages/dashboard/Users.tsx))
```tsx
- Create user form:
  * Name input
  * Email input
  * Password (minimum 8 characters)
  * Role selection (EMPLOYEE, ADMIN)
  * Auto-validation on field change
- Edit user form
- Delete confirmation dialog
```

#### Form Patterns

**Controlled Input Pattern**
```tsx
const [formData, setFormData] = useState({
  email: "",
  password: "",
});

const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  const { name, value } = e.target;
  setFormData(prev => ({ ...prev, [name]: value }));
};
```

**Error Handling**
- Display field-level errors
- Show API error messages
- Clear errors on input change
- Toast notifications for success/failure

**Loading States**
- Disable submit button during submission
- Show loading indicator
- Prevent multiple submissions

---

## Security Architecture

### 1. **Authentication System**

#### JWT (JSON Web Tokens) Implementation

**Token Generation** ([python_backend/routes/auth.py](python_backend/routes/auth.py))
```python
def generate_token(user_id, pharmacy_id):
    """Generate JWT token for user"""
    expires_at = datetime.now() + timedelta(hours=24)
    
    payload = {
        'user_id': user_id,
        'pharmacy_id': pharmacy_id,
        'exp': expires_at
    }
    
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
    
    # Store token in database for validation
    token_query = """
        INSERT INTO auth_tokens (user_id, token, expires_at)
        VALUES (%s, %s, %s)
    """
    execute_query(token_query, (user_id, token, expires_at))
    
    return token
```

**Key Features:**
- 24-hour expiration
- HS256 algorithm with SECRET_KEY
- Token stored in database for revocation support
- Issued on successful login

#### Token Management

**Client-Side Storage** ([client/lib/AuthContext.tsx](client/lib/AuthContext.tsx))
```tsx
// Store in localStorage
localStorage.setItem('auth_token', authToken);
localStorage.setItem('user', JSON.stringify(userData));

// Retrieve for API calls
const token = localStorage.getItem('auth_token');
```

**Token Transmission** ([client/lib/api.ts](client/lib/api.ts))
```typescript
// Request interceptor - attach JWT token
apiClient.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('auth_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    }
);
```

**Token Validation** ([python_backend/middleware.py](python_backend/middleware.py))
```python
def verify_token(token):
    """Verify JWT token and return user data"""
    try:
        # Decode JWT token
        payload = jwt.decode(
            token,
            Config.SECRET_KEY,
            algorithms=['HS256']
        )
        
        # Check if token exists in database and is valid
        token_query = """
            SELECT id, user_id, expires_at, is_valid
            FROM auth_tokens
            WHERE token = %s AND is_valid = TRUE
        """
        token_record = execute_query(token_query, (token,), fetch_one=True)
        
        if not token_record:
            return None
        
        # Check if token has expired
        if token_record['expires_at'] < datetime.now():
            # Invalidate expired token
            execute_query(
                "UPDATE auth_tokens SET is_valid = FALSE WHERE id = %s",
                (token_record['id'],)
            )
            return None
        
        # Get user details
        user_query = """
            SELECT u.id, u.name, u.email, u.role, u.pharmacy_id, u.is_active
            FROM users u
            WHERE u.id = %s
        """
        user = execute_query(user_query, (payload['user_id'],), fetch_one=True)
        
        return user
    except jwt.ExpiredSignatureError:
        logger.warning("Token has expired")
        return None
    except jwt.InvalidTokenError as e:
        logger.warning(f"Invalid token: {e}")
        return None
```

### 2. **Password Security**

#### Password Hashing

**Bcrypt Implementation** ([python_backend/routes/auth.py](python_backend/routes/auth.py))
```python
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
        return is_valid
    except Exception as e:
        logger.error(f"Password verification error: {type(e).__name__}: {e}")
        return False
```

**Key Features:**
- 12-round Bcrypt algorithm
- Secure encoding/decoding
- Error handling for edge cases

#### Password Requirements
- Minimum 8 characters
- Enforced at client and server level
- Password confirmation in signup

### 3. **Authorization & Access Control**

#### Role-Based Access Control (RBAC)

**Decorator Pattern** ([python_backend/middleware.py](python_backend/middleware.py))
```python
def require_role(*allowed_roles):
    """Decorator to require specific role(s) for a route"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # First check authentication
            token = get_token_from_header()
            
            if not token:
                return jsonify({'error': 'Authentication required', 'code': 'NO_TOKEN'}), 401
            
            user = verify_token(token)
            
            if not user:
                return jsonify({'error': 'Invalid or expired token', 'code': 'INVALID_TOKEN'}), 401
            
            # Check role
            if user['role'] not in allowed_roles:
                return jsonify({
                    'error': 'Access denied. Insufficient permissions.',
                    'code': 'INSUFFICIENT_PERMISSIONS',
                    'required_roles': list(allowed_roles),
                    'user_role': user['role']
                }), 403
            
            # Attach user to request context
            request.current_user = user
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator
```

**Usage Examples**
```python
@users_bp.route('/', methods=['POST'])
@require_role('ADMIN')
def create_user():
    """Create new user - Admin only"""
    pass

@users_bp.route('/<int:user_id>', methods=['GET'])
@require_auth
def get_user(user_id):
    """Get user - Any authenticated user"""
    pass
```

#### Roles
- **ADMIN**: Full access, can manage users
- **EMPLOYEE**: Limited access, operational tasks

#### Tenant Isolation
```python
# Check pharmacy_id to ensure data isolation
query = """
    SELECT * FROM users 
    WHERE id = %s AND pharmacy_id = %s
"""
user = execute_query(query, (user_id, current_user['pharmacy_id']))
```

### 4. **API Security**

#### Request Interceptor for 401 Handling

**Automatic Redirect on Token Expiry** ([client/lib/api.ts](client/lib/api.ts))
```typescript
// Response interceptor - handle 401 errors
apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            // Token expired or invalid
            localStorage.removeItem('auth_token');
            localStorage.removeItem('user');

            // Redirect to login if not already there
            if (window.location.pathname !== '/login' && window.location.pathname !== '/signup') {
                window.location.href = '/login';
            }
        }
        return Promise.reject(error);
    }
);
```

#### Token Extraction from Header

**Bearer Token Pattern** ([python_backend/middleware.py](python_backend/middleware.py))
```python
def get_token_from_header():
    """Extract JWT token from Authorization header"""
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    
    # Expected format: "Bearer <token>"
    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        return None
    
    return parts[1]
```

### 5. **Session Management**

**Token Logout/Invalidation** ([python_backend/routes/auth.py](python_backend/routes/auth.py))
```python
@auth_bp.route('/logout', methods=['POST'])
@require_auth
def logout():
    """Logout user and invalidate token"""
    try:
        from middleware import get_token_from_header
        token = get_token_from_header()
        
        if token:
            # Invalidate token in database
            execute_query(
                "UPDATE auth_tokens SET is_valid = FALSE WHERE token = %s",
                (token,)
            )
        
        return jsonify({'message': 'Logout successful'}), 200
    except Exception as e:
        logger.error(f"Error during logout: {e}")
        return jsonify({'error': 'Logout failed'}), 500
```

**Client-Side Logout** ([client/lib/AuthContext.tsx](client/lib/AuthContext.tsx))
```tsx
const logout = () => {
    // Call logout API (optional, to invalidate token on server)
    api.auth.logout().catch(() => {
        // Ignore errors, just clear local state
    });

    // Clear localStorage
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user');

    // Clear state
    setToken(null);
    setUser(null);

    // Redirect to login
    window.location.href = '/login';
};
```

### 6. **Protected Routes**

**Route Protection Component** ([client/components/ProtectedRoute.tsx](client/components/ProtectedRoute.tsx))
```tsx
// Checks authentication and authorization before rendering
// Redirects to login if not authenticated
```

---

## Validation Strategy

### 1. **Client-Side Validation**

#### Form Input Validation

**Email Validation**
```tsx
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
if (!emailRegex.test(formData.email)) {
  setError("Please enter a valid email address");
}
```

**Password Validation**
```tsx
// Minimum 8 characters
if (formData.password.length < 8) {
  setError("Password must be at least 8 characters");
}

// Password confirmation
if (formData.password !== formData.confirmPassword) {
  setError("Passwords do not match");
}

// Required fields
if (!formData.email || !formData.password) {
  setError("Email and password are required");
}
```

#### Real-Time Feedback

**Password Requirements Display**
```tsx
const passwordRequirements = [
  { label: "At least 8 characters", met: formData.password.length >= 8 },
  { label: "Contains uppercase letter", met: /[A-Z]/.test(formData.password) },
  { label: "Contains lowercase letter", met: /[a-z]/.test(formData.password) },
  { label: "Contains number", met: /[0-9]/.test(formData.password) },
];

// Display with visual indicators (checkmarks for met requirements)
```

#### HTML5 Input Types
```tsx
<input type="email" required />
<input type="password" required minLength={8} />
<input type="text" placeholder="Enter value" />
```

### 2. **Server-Side Validation**

#### Input Validation in Routes

**Login Endpoint** ([python_backend/routes/auth.py](python_backend/routes/auth.py))
```python
@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and return JWT token"""
    data = request.get_json()
    
    # Validate required fields
    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400
    
    # Verify password
    if not verify_password(data['current_password'], result['password']):
        return jsonify({'error': 'Current password is incorrect'}), 401
    
    # ... rest of logic
```

**User Creation Endpoint** ([python_backend/routes/users.py](python_backend/routes/users.py))
```python
@users_bp.route('/', methods=['POST'])
@require_role('ADMIN')
def create_user():
    """Create new user (Admin only)"""
    data = request.get_json()
    
    # Validate required fields
    if not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Name, email, and password are required'}), 400
    
    # Validate password strength
    if len(data['password']) < 8:
        return jsonify({'error': 'Password must be at least 8 characters'}), 400
    
    # Validate role
    role = data.get('role', 'EMPLOYEE')
    if role not in ['EMPLOYEE', 'ADMIN']:
        return jsonify({'error': 'Invalid role. Must be EMPLOYEE or ADMIN'}), 400
    
    # Check constraints (e.g., only one admin per pharmacy)
    if role == 'ADMIN':
        admin_check = execute_query(
            "SELECT COUNT(*) as count FROM users WHERE pharmacy_id = %s AND role = 'ADMIN'",
            (current_user['pharmacy_id'],),
            fetch_one=True
        )
        if admin_check['count'] > 0:
            return jsonify({'error': 'Only one admin allowed per pharmacy'}), 409
    
    # Hash password
    hashed_password = hash_password(data['password'])
    
    # ... insert into database
```

**Password Change Endpoint** ([python_backend/routes/auth.py](python_backend/routes/auth.py))
```python
@auth_bp.route('/change-password', methods=['POST'])
@require_auth
def change_password():
    """Change user password"""
    data = request.get_json()
    user = request.current_user
    
    # Validate required fields
    if not data.get('current_password') or not data.get('new_password'):
        return jsonify({'error': 'Current password and new password are required'}), 400
    
    # Verify current password
    password_query = "SELECT password FROM users WHERE id = %s"
    result = execute_query(password_query, (user['id'],), fetch_one=True)
    
    if not verify_password(data['current_password'], result['password']):
        return jsonify({'error': 'Current password is incorrect'}), 401
    
    # Validate new password
    if len(data['new_password']) < 8:
        return jsonify({'error': 'New password must be at least 8 characters'}), 400
    
    # Hash and update
    hashed_password = hash_password(data['new_password'])
    update_query = "UPDATE users SET password = %s WHERE id = %s"
    execute_query(update_query, (hashed_password, user['id']))
    
    return jsonify({'message': 'Password changed successfully'}), 200
```

### 3. **Data Integrity Validation**

#### Database Constraints
```sql
-- Email uniqueness
UNIQUE(email)

-- Pharmacy-user relationship
FOREIGN KEY (pharmacy_id) REFERENCES pharmacy(id)

-- Role constraints
CHECK (role IN ('ADMIN', 'EMPLOYEE'))

-- Active status
is_active BOOLEAN DEFAULT TRUE
```

#### Duplicate Prevention
```python
try:
    # Insert operation
    execute_query(query, params)
except Exception as e:
    if 'duplicate key' in str(e).lower() or 'unique' in str(e).lower():
        return jsonify({'error': 'Email already exists'}), 409
    return jsonify({'error': 'Failed to create user'}), 500
```

### 4. **Error Response Format**

**Standardized Error Responses**
```json
{
  "error": "Error message",
  "code": "ERROR_CODE"
}

{
  "error": "Access denied. Insufficient permissions.",
  "code": "INSUFFICIENT_PERMISSIONS",
  "required_roles": ["ADMIN"],
  "user_role": "EMPLOYEE"
}
```

### 5. **Logging & Monitoring**

**Error Logging** ([python_backend/routes/users.py](python_backend/routes/users.py))
```python
logger.error(f"Error creating user: {e}")
logger.warning("Token has expired")
logger.debug(f"Password verification result: {is_valid}")
```

---

## Security Summary

| Component | Implementation |
|-----------|-----------------|
| Authentication | JWT with 24-hour expiration |
| Password Hashing | Bcrypt with 12 rounds |
| Token Storage | Database + localStorage |
| Authorization | Role-based access control (RBAC) |
| Session Management | Token invalidation on logout |
| Input Validation | Client-side + Server-side |
| Data Isolation | Tenant-aware queries |
| Error Handling | Standardized error responses |
| Token Transmission | Bearer scheme in Authorization header |

---

## Validation Summary

| Layer | Validation Type |
|-------|-----------------|
| **Client** | Email format, password strength, required fields, regex patterns |
| **Server** | Field presence, password strength, role validation, business rules |
| **Database** | Unique constraints, foreign keys, domain constraints |

---

## Best Practices Implemented

✅ **Never log passwords**
✅ **Always hash passwords with salt**
✅ **Validate on both client and server**
✅ **Use HTTPS in production**
✅ **Expire tokens appropriately**
✅ **Implement logout/token invalidation**
✅ **Use environment variables for secrets**
✅ **Check user permissions per request**
✅ **Sanitize user inputs**
✅ **Handle errors gracefully without exposing details**
