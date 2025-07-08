from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from typing import Optional, Union

from config.database import get_db
from database.models.user import User
from auth.jwt_handler import JWTHandler
from services.auth_service import AuthService
from utils.exceptions import AuthenticationError
from database.schemas.user import UserSignin

# HTTP Bearer token scheme
security_bearer = HTTPBearer()
# HTTP Basic auth scheme
security_basic = HTTPBasic()

# Combined security scheme for docs
from fastapi.security.base import SecurityBase
from fastapi.security.utils import get_authorization_scheme_param
from fastapi import Request
from fastapi.openapi.models import HTTPBase as HTTPBaseModel

def get_current_user_bearer(
    credentials: HTTPAuthorizationCredentials = Depends(security_bearer),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current authenticated user from JWT Bearer token
    
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

def get_current_user_basic(
    credentials: HTTPBasicCredentials = Depends(security_basic),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current authenticated user from HTTP Basic Auth (email/password)
    
    Args:
        credentials: HTTP Basic credentials
        db: Database session
        
    Returns:
        Current authenticated user
        
    Raises:
        HTTPException: If authentication fails
    """
    try:
        # Use email as username and password from Basic Auth
        user_signin = UserSignin(
            email=credentials.username,
            password=credentials.password
        )
        
        # Initialize auth service
        auth_service = AuthService(db)
        
        # Authenticate user (this will verify password and return user info)
        auth_response = auth_service.signin(user_signin)
        
        # Get user from database
        user = db.query(User).filter(User.email == credentials.username).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Basic"}
            )
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Basic"}
        )

def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> User:
    """
    Get current authenticated user from either Bearer token or Basic Auth
    
    Args:
        request: FastAPI request object
        db: Database session
        
    Returns:
        Current authenticated user
        
    Raises:
        HTTPException: If authentication fails
    """
    # Check Authorization header to determine auth type
    auth_header = request.headers.get("authorization")
    
    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer, Basic"}
        )
    
    if auth_header.startswith("Bearer "):
        # Use Bearer token authentication
        try:
            token = auth_header.split(" ")[1]
            auth_service = AuthService(db)
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
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )
    
    elif auth_header.startswith("Basic "):
        # Use Basic Auth authentication
        try:
            import base64
            encoded_credentials = auth_header.split(" ")[1]
            decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8")
            username, password = decoded_credentials.split(":", 1)
            
            user_signin = UserSignin(email=username, password=password)
            auth_service = AuthService(db)
            
            # This will throw AuthenticationError if credentials are invalid
            auth_response = auth_service.signin(user_signin)
            
            # If we get here, authentication was successful
            # Get the user from the auth_response (which contains the authenticated user)
            user = db.query(User).filter(User.email == username).first()
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication credentials",
                    headers={"WWW-Authenticate": "Basic"}
                )
            
            return user
            
        except AuthenticationError as e:
            # Handle authentication errors specifically
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=e.message,
                headers={"WWW-Authenticate": "Basic"}
            )
        except HTTPException:
            raise
        except Exception as e:
            # Handle other errors (malformed auth header, etc.)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Basic"}
            )
    
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme",
            headers={"WWW-Authenticate": "Bearer, Basic"}
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
    request: Request,
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Get current user if authenticated, otherwise return None
    
    Args:
        request: FastAPI request object
        db: Database session
        
    Returns:
        Current user or None if not authenticated
    """
    try:
        # Try to get current user, but don't raise exception if fails
        return get_current_user(request, db)
    except HTTPException:
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