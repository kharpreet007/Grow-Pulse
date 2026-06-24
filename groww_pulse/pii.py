import re
from typing import Tuple

# Regex patterns for PII detection
EMAIL_REGEX = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
# Matches international and Indian phone numbers. e.g. +91 9876543210, 9876543210, 09876543210, etc.
PHONE_REGEX = re.compile(r'(\+?\d{1,3}[\s-]?)?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{4}')
# Aadhaar format: 12 digits, optional spaces/hyphens like XXXX XXXX XXXX or XXXX-XXXX-XXXX
AADHAAR_REGEX = re.compile(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}\b')
# PAN format: 5 uppercase letters, 4 digits, 1 uppercase letter
PAN_REGEX = re.compile(r'\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b')

def scrub_pii(text: str) -> Tuple[str, int]:
    """
    Scrubs PII from the given text.
    Returns the scrubbed text and the number of redactions made.
    """
    if not text:
        return text, 0
        
    redactions = 0
    
    def replacer(match) -> str:
        nonlocal redactions
        redactions += 1
        return '[REDACTED]'

    # Apply all regex patterns, replacing matches with [REDACTED]
    text = EMAIL_REGEX.sub(replacer, text)
    text = PHONE_REGEX.sub(replacer, text)
    text = AADHAAR_REGEX.sub(replacer, text)
    text = PAN_REGEX.sub(replacer, text)
    
    return text, redactions
