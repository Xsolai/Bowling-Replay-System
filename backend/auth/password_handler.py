from passlib.context import CryptContext
from passlib.hash import bcrypt
import secrets
import string

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class PasswordHandler:
    """Handle password hashing and verification"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using bcrypt
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password string
        """
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash
        
        Args:
            plain_password: Plain text password
            hashed_password: Hashed password from database
            
        Returns:
            True if password matches, False otherwise
        """
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def generate_secure_token(length: int = 32) -> str:
        """
        Generate a secure random token
        
        Args:
            length: Length of the token to generate
            
        Returns:
            Secure random token string
        """
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    @staticmethod
    def is_password_strong(password: str) -> tuple[bool, str]:
        """
        Check if password meets security requirements
        
        Args:
            password: Password to check
            
        Returns:
            Tuple of (is_strong, error_message)
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        if not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter"
        
        if not any(c.islower() for c in password):
            return False, "Password must contain at least one lowercase letter"
        
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one number"
        
        # Check for common patterns
        common_patterns = ['123456', 'password', 'qwerty', 'abc123']
        if any(pattern in password.lower() for pattern in common_patterns):
            return False, "Password contains common patterns"
        
        return True, "Password is strong" 