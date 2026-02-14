/**
 * Validation utility functions for checking account application
 * Each validator returns { valid: boolean, message: string }
 */

const US_STATES = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY',
    'DC'
];

export function validateFirstName(value) {
    const v = (value || '').trim();
    if (!v) return { valid: false, message: 'First name is required.' };
    if (v.length < 2 || v.length > 50) return { valid: false, message: 'First name must be 2–50 characters.' };
    if (!/^[a-zA-Z\s'-]+$/.test(v)) return { valid: false, message: 'First name can only contain letters, spaces, hyphens, and apostrophes.' };
    return { valid: true, message: '' };
}

export function validateLastName(value) {
    const v = (value || '').trim();
    if (!v) return { valid: false, message: 'Last name is required.' };
    if (v.length < 2 || v.length > 50) return { valid: false, message: 'Last name must be 2–50 characters.' };
    if (!/^[a-zA-Z\s'-]+$/.test(v)) return { valid: false, message: 'Last name can only contain letters, spaces, hyphens, and apostrophes.' };
    return { valid: true, message: '' };
}

export function validateEmail(value) {
    const v = (value || '').trim();
    if (!v) return { valid: false, message: 'Email address is required.' };
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(v)) return { valid: false, message: 'Please enter a valid email address.' };
    return { valid: true, message: '' };
}

export function validatePhone(value) {
    const digits = (value || '').replace(/\D/g, '');
    if (!digits) return { valid: false, message: 'Phone number is required.' };
    if (digits.length !== 10) return { valid: false, message: 'Phone number must be exactly 10 digits.' };
    return { valid: true, message: '' };
}

export function validateDateOfBirth(value) {
    const v = (value || '').trim();
    if (!v) return { valid: false, message: 'Date of birth is required.' };

    // Accepts MM/DD/YYYY or YYYY-MM-DD
    let date;
    if (/^\d{2}\/\d{2}\/\d{4}$/.test(v)) {
        const [month, day, year] = v.split('/').map(Number);
        date = new Date(year, month - 1, day);
        if (date.getMonth() !== month - 1 || date.getDate() !== day) {
            return { valid: false, message: 'Please enter a valid date (MM/DD/YYYY).' };
        }
    } else if (/^\d{4}-\d{2}-\d{2}$/.test(v)) {
        const [year, month, day] = v.split('-').map(Number);
        date = new Date(year, month - 1, day);
        if (date.getMonth() !== month - 1 || date.getDate() !== day) {
            return { valid: false, message: 'Please enter a valid date (YYYY-MM-DD).' };
        }
    } else {
        return { valid: false, message: 'Please enter date in MM/DD/YYYY format.' };
    }

    const today = new Date();
    let age = today.getFullYear() - date.getFullYear();
    const monthDiff = today.getMonth() - date.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < date.getDate())) age--;

    if (age < 18) return { valid: false, message: 'You must be at least 18 years old to open an account.' };
    if (age > 120) return { valid: false, message: 'Please enter a valid date of birth.' };

    return { valid: true, message: '' };
}

export function validateSSN(value) {
    const digits = (value || '').replace(/\D/g, '');
    if (!digits) return { valid: false, message: 'Social Security Number is required.' };
    if (digits.length !== 9) return { valid: false, message: 'SSN must be exactly 9 digits.' };
    // Basic invalid SSN checks
    if (digits.startsWith('000') || digits.startsWith('666') || digits.startsWith('9')) {
        return { valid: false, message: 'Please enter a valid SSN.' };
    }
    return { valid: true, message: '' };
}

export function validateStreet(value) {
    const v = (value || '').trim();
    if (!v) return { valid: false, message: 'Street address is required.' };
    if (v.length < 5 || v.length > 100) return { valid: false, message: 'Street address must be 5–100 characters.' };
    return { valid: true, message: '' };
}

export function validateCity(value) {
    const v = (value || '').trim();
    if (!v) return { valid: false, message: 'City is required.' };
    if (!/^[a-zA-Z\s'-]+$/.test(v)) return { valid: false, message: 'City can only contain letters and spaces.' };
    return { valid: true, message: '' };
}

export function validateState(value) {
    const v = (value || '').trim().toUpperCase();
    if (!v) return { valid: false, message: 'State is required.' };
    if (!US_STATES.includes(v)) return { valid: false, message: 'Please enter a valid 2-letter US state code (e.g., CA, NY, TX).' };
    return { valid: true, message: '' };
}

export function validateZip(value) {
    const v = (value || '').trim();
    if (!v) return { valid: false, message: 'ZIP code is required.' };
    if (!/^\d{5}$/.test(v)) return { valid: false, message: 'ZIP code must be exactly 5 digits.' };
    return { valid: true, message: '' };
}

export function formatPhone(digits) {
    const d = digits.replace(/\D/g, '');
    if (d.length <= 3) return d;
    if (d.length <= 6) return `(${d.slice(0, 3)}) ${d.slice(3)}`;
    return `(${d.slice(0, 3)}) ${d.slice(3, 6)}-${d.slice(6, 10)}`;
}

export function maskSSN(value) {
    const digits = (value || '').replace(/\D/g, '');
    if (digits.length <= 4) return digits;
    return '•••-••-' + digits.slice(5);
}
