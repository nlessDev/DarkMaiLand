class SMTPXError(Exception):
    """Base exception class"""
    
class ProtocolError(SMTPXError):
    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__(f"{code} {message}")

class CryptoError(SMTPXError):
    """Cryptography-related errors"""

class DatabaseError(SMTPXError):
    """Database operation failures"""

class RateLimitExceeded(SMTPXError):
    """Rate limiting enforcement"""
