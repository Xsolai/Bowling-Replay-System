from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from pydantic import BaseModel
import os

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here-make-it-secure")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

class TokenData(BaseModel):
    user_id: Optional[str] = None
    email: Optional[str] = None

class JWTHandler:
    """Handle JWT token operations"""
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Create a JWT access token
        
        Args:
            data: Dictionary containing user data
            expires_delta: Optional custom expiration time
            
        Returns:
            JWT token string
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def create_refresh_token(data: dict) -> str:
        """
        Create a JWT refresh token
        
        Args:
            data: Dictionary containing user data
            
        Returns:
            JWT refresh token string
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> Optional[Dict[str, Any]]:
        """
        Verify and decode a JWT token
        
        Args:
            token: JWT token string
            
        Returns:
            Decoded token payload or None if invalid
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            return None
    
    @staticmethod
    def decode_token(token: str) -> Optional[TokenData]:
        """
        Decode JWT token and extract user data
        
        Args:
            token: JWT token string
            
        Returns:
            TokenData object or None if invalid
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")
            email: str = payload.get("email")
            
            if user_id is None:
                return None
            
            return TokenData(user_id=user_id, email=email)
        except JWTError:
            return None
    
    @staticmethod
    def is_token_expired(token: str) -> bool:
        """
        Check if a token is expired
        
        Args:
            token: JWT token string
            
        Returns:
            True if token is expired, False otherwise
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            exp_timestamp = payload.get("exp")
            
            if exp_timestamp is None:
                return True
            
            exp_datetime = datetime.utcfromtimestamp(exp_timestamp)
            return datetime.utcnow() > exp_datetime
        except JWTError:
            return True
    
    @staticmethod
    def get_token_type(token: str) -> Optional[str]:
        """
        Get the type of token (access or refresh)
        
        Args:
            token: JWT token string
            
        Returns:
            Token type or None if invalid
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload.get("type")
        except JWTError:
            return None
    
    @staticmethod
    def create_email_verification_token(email: str) -> str:
        """
        Create a token for email verification
        
        Args:
            email: User email address
            
        Returns:
            Email verification token
        """
        expire = datetime.utcnow() + timedelta(hours=24)  # 24 hours for email verification
        to_encode = {
            "email": email,
            "exp": expire,
            "type": "email_verification"
        }
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    @staticmethod
    def verify_email_verification_token(token: str) -> Optional[str]:
        """
        Verify email verification token and extract email
        
        Args:
            token: Email verification token
            
        Returns:
            Email address or None if invalid
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            
            if payload.get("type") != "email_verification":
                return None
            
            return payload.get("email")
        except JWTError:
            return None
    
    @staticmethod
    def create_password_reset_token(email: str) -> str:
        """
        Create a token for password reset
        
        Args:
            email: User email address
            
        Returns:
            Password reset token
        """
        expire = datetime.utcnow() + timedelta(hours=1)  # 1 hour for password reset
        to_encode = {
            "email": email,
            "exp": expire,
            "type": "password_reset"
        }
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    @staticmethod
    def verify_password_reset_token(token: str) -> Optional[str]:
        """
        Verify password reset token and extract email
        
        Args:
            token: Password reset token
            
        Returns:
            Email address or None if invalid
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            
            if payload.get("type") != "password_reset":
                return None
            
            return payload.get("email")
        except JWTError:
            return None 