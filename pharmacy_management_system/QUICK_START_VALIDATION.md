# Quick Reference - Validations

## What was implemented?

When creating or updating **customers or users**, the system now validates:

### 1. Indian Mobile Number Validation ☎️
Checks that phone numbers are valid Indian mobile numbers:
- **Length**: Exactly 10 digits
- **Prefix**: Must start with 6, 7, 8, or 9
- **Format accepted**: 
  - `9876543210` ✅
  - `+91 9876543210` ✅
  - `+91-9876543210` ✅
  - `91 98 765 43210` ✅

### 2. Age Verification (18+ years) 🎂
Validates date of birth ensures person is 18 or older:
- **Format**: YYYY-MM-DD
- **Rules**:
  - Must be exactly 18 or older
  - Cannot be in the future
  - Example valid DOB: `1990-01-15` (if person is 35+ years old)
  - Example invalid DOB: `2010-06-15` (would be only 15-16 years old)

## How to use?

### Add a Customer via UI
1. Click "Add Customer" button
2. Fill in required fields:
   - **Name** - Required
   - **Phone** - Validates as Indian number if provided
   - **Date of Birth** - Validates 18+ age requirement if provided
   - **Email** - Validates email format if provided
3. System shows validation errors immediately
4. Click "Create Customer" when all fields are valid

### Add a Staff Member/Employee
1. Go to Settings → Team/Users
2. Click "Add User" or "Create Employee"
3. Fill required fields:
   - **Name** - Required
   - **Email** - Required (unique)
   - **Password** - Min 8 characters
   - **Phone** - Validates as Indian number if provided
   - **DOB** - Validates 18+ if provided
4. System validates before submission

## Error Messages You'll See

| Scenario | Error Message |
|----------|---------------|
| Phone is too short | `"Invalid phone number format. Indian mobile numbers should be 10 digits"` |
| Phone starts with 0-5 | `"Invalid phone number. Mobile numbers should start with 6, 7, 8, or 9"` |
| Person under 18 | `"User must be at least 18 years old (Currently X years old)"` |
| Future date of birth | `"Date of birth cannot be in the future"` |
| Wrong date format | `"Invalid date format. Please use YYYY-MM-DD format"` |
| Invalid email | `"Invalid email format"` |

## Where the validation happens?

**Frontend** 🖥️
- Instant feedback as you type
- Shows errors before API call
- File: `client/lib/validation.ts`

**Backend** 🔒
- Final validation gate
- Prevents invalid data in database
- File: `python_backend/validators.py`

Both use identical logic for consistency!

## Examples

### ✅ Valid Customer
```
Name: Rajesh Kumar
Phone: 9876543210
DOB: 2000-01-15 (26 years old)
Email: rajesh@email.com
```

### ❌ Invalid Customer (Would show error)
```
Name: Aisha Khan
Phone: 5123456789 ← Starts with 5, not valid mobile prefix
DOB: 2010-06-15 ← Would be only 15 years old
Email: aisha@invalid ← Missing domain extension
```

### ✅ Valid Phone Formats
- `9876543210`
- `+919876543210`
- `+91-9876543210`
- `+91 98 765 43210`
- `91 9876543210`

### ❌ Invalid Phone Formats
- `8765432109` ← Starts with 8... wait, 8 is valid! This would work
- `5123456789` ← Starts with 5, NOT valid
- `98765432` ← Too short (8 digits)
- `abcdefghij` ← Contains letters

## Testing

To verify validations work, run:
```bash
cd python_backend
python test_validations.py
```

This runs 8 test cases covering all scenarios.

## For Developers

### Import validation functions:
```python
# Backend
from validators import validate_indian_mobile, validate_age_18_plus

# Frontend
import { validateIndianMobile, validateAge18Plus } from "@/lib/validation"
```

### Use in code:
```python
# Backend
is_valid, error_msg = validate_indian_mobile("9876543210")
is_valid, error_msg = validate_age_18_plus("2000-01-15")
```

```typescript
// Frontend
const result = validateIndianMobile("9876543210");
if (!result.valid) {
  console.log("Error:", result.error);
}
```

---

**Last Updated**: February 4, 2026
**Status**: ✅ Fully Implemented and Tested
