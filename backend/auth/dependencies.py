from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional

from config.database import get_db
from database.models.user import User
from auth.jwt_handler import JWTHandler
from services.auth_service import AuthService
from utils.exceptions import AuthenticationError

# HTTP Bearer token scheme
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current authenticated user from JWT token
    
    Args:
        credentials: HTTP Authorization credentials
        db: Database session
        
    Returns:
        Current authenticated user
        
    Raises:
        HTTPException: If authentication fails
    """
    try:
        # Extract token from credentials
        token = credentials.credentials
        
        # Initialize auth service
        auth_service = AuthService(db)
        
        # Get user from token
        user = auth_service.get_current_user(token)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account is disabled",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        if not user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email not verified",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current active user (wrapper for get_current_user)
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Current active user
    """
    return current_user

def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Get current user if authenticated, otherwise return None
    
    Args:
        credentials: Optional HTTP Authorization credentials
        db: Database session
        
    Returns:
        Current user or None if not authenticated
    """
    if not credentials:
        return None
    
    try:
        token = credentials.credentials
        auth_service = AuthService(db)
        user = auth_service.get_current_user(token)
        
        if user and user.is_active and user.is_verified:
            return user
        
        return None
        
    except Exception:
        return None

def require_verified_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Require user to have verified email
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Verified user
        
    Raises:
        HTTPException: If user email is not verified
    """
    if not current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email verification required"
        )
    
    return current_user

def require_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Require user to have admin privileges
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Admin user
        
    Raises:
        HTTPException: If user is not admin
    """
    # Note: You would need to add an 'is_admin' field to the User model
    # For now, this is a placeholder implementation
    if not getattr(current_user, 'is_admin', False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    
    return current_user

async def validate_token(token: str, db: Session) -> Optional[User]:
    """
    Validate JWT token and return user
    
    Args:
        token: JWT token string
        db: Database session
        
    Returns:
        User object or None if invalid
    """
    try:
        jwt_handler = JWTHandler()
        token_data = jwt_handler.decode_token(token)
        
        if not token_data:
            return None
        
        user = db.query(User).filter(User.id == token_data.user_id).first()
        
        if user and user.is_active and user.is_verified:
            return user
        
        return None
        
    except Exception:
        return None

class AuthRequired:
    """Dependency class for requiring authentication"""
    
    def __init__(self, require_verification: bool = True):
        self.require_verification = require_verification
    
    def __call__(self, current_user: User = Depends(get_current_user)) -> User:
        if self.require_verification and not current_user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Email verification required"
            )
        
        return current_user

class OptionalAuth:
    """Dependency class for optional authentication"""
    
    def __call__(self, current_user: Optional[User] = Depends(get_optional_current_user)) -> Optional[User]:
        return current_user

# Convenience instances
auth_required = AuthRequired()
auth_required_unverified = AuthRequired(require_verification=False)
optional_auth = OptionalAuth() 