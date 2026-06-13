/**
 * Frontend validation utilities
 * Validates Indian mobile numbers and age (18+)
 */

export function validateIndianMobile(phone: string): { valid: boolean; error: string } {
  if (!phone) {
    return { valid: false, error: "Phone number is required" };
  }

  // Remove all spaces and special characters except digits and +
  const cleaned = phone.replace(/[^\d+]/g, "");

  // Check if it starts with +91 or 91 or 0
  let digitsOnly = cleaned;
  if (cleaned.startsWith("+91")) {
    digitsOnly = cleaned.slice(3);
  } else if (cleaned.startsWith("91")) {
    digitsOnly = cleaned.slice(2);
  } else if (cleaned.startsWith("0")) {
    digitsOnly = cleaned.slice(1);
  }

  // Valid Indian mobile should be exactly 10 digits
  if (!/^\d{10}$/.test(digitsOnly)) {
    return {
      valid: false,
      error: "Invalid phone number format. Indian mobile numbers should be 10 digits",
    };
  }

  // Check if it's a valid mobile number prefix (6-9 for mobile)
  if (!["6", "7", "8", "9"].includes(digitsOnly[0])) {
    return {
      valid: false,
      error: "Invalid phone number. Mobile numbers should start with 6, 7, 8, or 9",
    };
  }

  return { valid: true, error: "" };
}

export function validateAge18Plus(dobStr: string): { valid: boolean; error: string } {
  if (!dobStr) {
    return { valid: false, error: "Date of birth is required" };
  }

  try {
    const dob = new Date(dobStr);
    
    // Check if date is valid
    if (isNaN(dob.getTime())) {
      return {
        valid: false,
        error: "Invalid date format. Please use YYYY-MM-DD format",
      };
    }

    // Check if date is in the future
    if (dob > new Date()) {
      return {
        valid: false,
        error: "Date of birth cannot be in the future",
      };
    }

    // Calculate age
    const today = new Date();
    let age = today.getFullYear() - dob.getFullYear();
    const monthDiff = today.getMonth() - dob.getMonth();

    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < dob.getDate())) {
      age--;
    }

    // Check if age is at least 18
    if (age < 18) {
      return {
        valid: false,
        error: `User must be at least 18 years old (Currently ${age} years old)`,
      };
    }

    return { valid: true, error: "" };
  } catch (error) {
    return {
      valid: false,
      error: "Error calculating age. Please check your date format",
    };
  }
}

export function validateCustomerForm(data: {
  name: string;
  email?: string;
  phone?: string;
  date_of_birth?: string;
}): { valid: boolean; errors: string[] } {
  const errors: string[] = [];

  if (!data.name || !data.name.trim()) {
    errors.push("Customer name is required");
  }

  if (data.phone && data.phone.trim()) {
    const phoneValidation = validateIndianMobile(data.phone);
    if (!phoneValidation.valid) {
      errors.push(phoneValidation.error);
    }
  }

  if (data.date_of_birth && data.date_of_birth.trim()) {
    const ageValidation = validateAge18Plus(data.date_of_birth);
    if (!ageValidation.valid) {
      errors.push(ageValidation.error);
    }
  }

  if (data.email && data.email.trim()) {
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!emailRegex.test(data.email)) {
      errors.push("Invalid email format");
    }
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}
