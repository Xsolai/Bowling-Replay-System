from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPBasic
from sqlalchemy.orm import Session

from config.database import get_db
from database.schemas.user import (
    UserSignup, UserSignin, UserResponse, AuthResponse, 
    EmailVerification, EmailVerificationResponse, 
    PasswordResetRequest, PasswordReset, MessageResponse
)
from services.auth_service import AuthService
from utils.exceptions import (
    ValidationError, AuthenticationError, 
    NotFoundError, BaseCustomException
)
from auth.dependencies import get_current_user

router = APIRouter()

@router.post("/signup", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    user_data: UserSignup,
    db: Session = Depends(get_db)
):
    """
    Register a new user
    
    - **email**: User email address (must be unique)
    - **name**: User full name
    - **password**: Strong password (min 8 chars, uppercase, lowercase, number)
    
    Returns:
    - Success message with instructions to check email
    """
    try:
        auth_service = AuthService(db)
        user_response, message = auth_service.signup(user_data)
        
        return MessageResponse(
            message=message,
            success=True
        )
        
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.message
        )
    except BaseCustomException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

@router.post("/signin", response_model=AuthResponse)
async def signin(
    credentials: UserSignin,
    db: Session = Depends(get_db)
):
    """
    Sign in a user
    
    - **email**: User email address
    - **password**: User password
    
    Returns:
    - Access token and user information
    """
    try:
        auth_service = AuthService(db)
        auth_response = auth_service.signin(credentials)
        
        return auth_response
        
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"}
        )
    except BaseCustomException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

@router.post("/verify-email", response_model=EmailVerificationResponse)
async def verify_email(
    verification_data: EmailVerification,
    db: Session = Depends(get_db)
):
    """
    Verify user email with token
    
    - **token**: Email verification token from email link
    
    Returns:
    - Verification success and automatic signin with access token
    """
    try:
        auth_service = AuthService(db)
        verification_response = auth_service.verify_email(verification_data.token)
        
        return verification_response
        
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.message
        )
    except BaseCustomException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

@router.post("/resend-verification", response_model=MessageResponse)
async def resend_verification_email(
    email_data: dict,
    db: Session = Depends(get_db)
):
    """
    Resend verification email
    
    - **email**: User email address
    
    Returns:
    - Success message
    """
    try:
        email = email_data.get("email")
        if not email:
            raise ValidationError("Email is required")
        
        auth_service = AuthService(db)
        message = auth_service.resend_verification_email(email)
        
        return MessageResponse(
            message=message,
            success=True
        )
        
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.message
        )
    except BaseCustomException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

@router.post("/forgot-password", response_model=MessageResponse)
async def request_password_reset(
    reset_request: PasswordResetRequest,
    db: Session = Depends(get_db)
):
    """
    Request password reset
    
    - **email**: User email address
    
    Returns:
    - Success message with instructions to check email
    """
    try:
        auth_service = AuthService(db)
        message = auth_service.request_password_reset(reset_request.email)
        
        return MessageResponse(
            message=message,
            success=True
        )
        
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.message
        )
    except BaseCustomException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

@router.post("/reset-password", response_model=MessageResponse)
async def reset_password(
    reset_data: PasswordReset,
    db: Session = Depends(get_db)
):
    """
    Reset user password
    
    - **token**: Password reset token from email
    - **new_password**: New strong password
    
    Returns:
    - Success message
    """
    try:
        auth_service = AuthService(db)
        message = auth_service.reset_password(reset_data.token, reset_data.new_password)
        
        return MessageResponse(
            message=message,
            success=True
        )
        
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.message
        )
    except BaseCustomException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

@router.post("/refresh-token", response_model=AuthResponse)
async def refresh_access_token(
    refresh_token_data: dict,
    db: Session = Depends(get_db)
):
    """
    Refresh access token
    
    - **refresh_token**: Valid refresh token
    
    Returns:
    - New access token and user information
    """
    try:
        refresh_token = refresh_token_data.get("refresh_token")
        if not refresh_token:
            raise ValidationError("Refresh token is required")
        
        auth_service = AuthService(db)
        auth_response = auth_service.refresh_token(refresh_token)
        
        return auth_response
        
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"}
        )
    except BaseCustomException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get current user information
    
    **Authentication Required:**
    - Use Bearer token: `Bearer <your-jwt-token>`
    - Or Basic auth: username=email, password=your-password
    
    Returns:
    - Current user profile information
    """
    try:
        user_response = UserResponse.from_orm(current_user)
        return user_response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

# Health check endpoint
@router.get("/health")
async def auth_health_check():
    """
    Authentication service health check
    """
    return {"status": "healthy", "service": "authentication"} 