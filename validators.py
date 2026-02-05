"""Input validation functions for Surakshita"""
import re
from typing import Tuple, Optional

def validate_coordinates(latitude: float, longitude: float) -> Tuple[bool, Optional[str]]:
    """
    Validate GPS coordinates - Restricted to India only
    
    Args:
        latitude: Latitude value
        longitude: Longitude value
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        lat = float(latitude)
        lon = float(longitude)
        
        # Strict bounding box for India geographic limits
        if not (6.0 <= lat <= 38.0) or not (68.0 <= lon <= 98.0):
            return False, "Services are currently only available within India."
        
        return True, None
    
    except (ValueError, TypeError):
        return False, "Invalid coordinate format"


def validate_description(description: str, max_length: int = 500) -> Tuple[bool, Optional[str]]:
    """
    Validate incident description
    
    Args:
        description: User-provided description
        max_length: Maximum allowed length
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not description or not description.strip():
        return False, "Description cannot be empty"
    
    if len(description) > max_length:
        return False, f"Description must be {max_length} characters or less"
    
    # Check for suspicious patterns
    suspicious_patterns = [
        r'<script[^>]*>',  # Script tags
        r'javascript:',     # JavaScript protocol
        r'on\w+\s*=',      # Event handlers (onclick, onerror, etc.)
    ]
    
    for pattern in suspicious_patterns:
        if re.search(pattern, description, re.IGNORECASE):
            return False, "Description contains invalid content"
    
    return True, None


def validate_incident_type(incident_type: str) -> Tuple[bool, Optional[str]]:
    """
    Validate incident type against whitelist
    
    Args:
        incident_type: Reported incident type
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    allowed_types = {
        'Harassment', 'Stalking', 'Assault', 'Theft', 
        'Suspicious Activity', 'Unsafe Area', 'Other',
        'SOS Emergency', 'Emergency', 'Threat'
    }
    
    if incident_type not in allowed_types:
        return False, f"Invalid incident type. Must be one of: {', '.join(allowed_types)}"
    
    return True, None


def sanitize_string(text: str, max_length: int = 500) -> str:
    """
    Sanitize user input by removing dangerous characters
    
    Args:
        text: Input string
        max_length: Maximum length
    
    Returns:
        Sanitized string
    """
    if not text:
        return ""
    
    # Remove null bytes
    text = text.replace('\x00', '')
    
    # Strip whitespace
    text = text.strip()
    
    # Truncate to max length
    text = text[:max_length]
    
    return text


def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    """
    Validate email format
    
    Args:
        email: Email address
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        return False, "Invalid email format"
    
    if len(email) > 254:  # RFC 5321
        return False, "Email address too long"
    
    return True, None


def validate_username(username: str) -> Tuple[bool, Optional[str]]:
    """
    Validate username
    
    Args:
        username: Username
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not username or len(username) < 3:
        return False, "Username must be at least 3 characters"
    
    if len(username) > 50:
        return False, "Username must be 50 characters or less"
    
    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        return False, "Username can only contain letters, numbers, underscores, and hyphens"
    
    return True, None


def validate_password(password: str) -> Tuple[bool, Optional[str]]:
    """
    Validate password strength
    
    Args:
        password: Password
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    if len(password) > 128:
        return False, "Password must be 128 characters or less"
    
    # Check for complexity
    has_upper = bool(re.search(r'[A-Z]', password))
    has_lower = bool(re.search(r'[a-z]', password))
    has_digit = bool(re.search(r'\d', password))
    
    if not (has_upper and has_lower and has_digit):
        return False, "Password must contain uppercase, lowercase, and numbers"
    
    return True, None
