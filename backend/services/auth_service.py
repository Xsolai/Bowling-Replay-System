from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, timedelta
from typing import Optional, Tuple
import uuid

from database.models.user import User
from database.schemas.user import UserSignup, UserSignin, UserResponse, AuthResponse, EmailVerificationResponse
from auth.password_handler import PasswordHandler
from auth.jwt_handler import JWTHandler
from services.email_service import EmailService
from utils.exceptions import AuthenticationError, ValidationError

class AuthService:
    """Handle authentication operations"""
    
    def __init__(self, db: Session):
        self.db = db
        self.password_handler = PasswordHandler()
        self.jwt_handler = JWTHandler()
        self.email_service = EmailService()
    
    def signup(self, user_data: UserSignup) -> Tuple[UserResponse, str]:
        """
        Register a new user
        
        Args:
            user_data: User registration data
            
        Returns:
            Tuple of (user_response, message)
            
        Raises:
            ValidationError: If validation fails
        """
        # Check if user already exists
        existing_user = self.db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            if existing_user.is_verified:
                raise ValidationError("Email already registered")
            else:
                # User exists but not verified, resend verification email
                # Generate new verification token
                verification_token = self.password_handler.generate_secure_token(32)
                verification_expires = datetime.utcnow() + timedelta(hours=24)
                
                # Update user with new verification token and password (in case they changed it)
                existing_user.verification_token = verification_token
                existing_user.verification_token_expires = verification_expires
                existing_user.password_hash = self.password_handler.hash_password(user_data.password)
                existing_user.name = user_data.name  # Update name in case it changed
                
                self.db.commit()
                self.db.refresh(existing_user)
                
                # Send verification email
                try:
                    self.email_service.send_verification_email(
                        to_email=existing_user.email,
                        name=existing_user.name,
                        verification_token=verification_token
                    )
                except Exception as e:
                    print(f"Error sending verification email: {e}")
                    # Don't fail registration if email fails
                
                user_response = UserResponse.from_orm(existing_user)
                return user_response, "Verification email sent. Please check your email for verification."
        
        # Validate password strength
        is_strong, message = self.password_handler.is_password_strong(user_data.password)
        if not is_strong:
            raise ValidationError(message)
        
        # Hash password
        password_hash = self.password_handler.hash_password(user_data.password)
        
        # Generate verification token
        verification_token = self.password_handler.generate_secure_token(32)
        verification_expires = datetime.utcnow() + timedelta(hours=24)
        
        # Create new user
        new_user = User(
            id=str(uuid.uuid4()),
            email=user_data.email,
            name=user_data.name,
            password_hash=password_hash,
            verification_token=verification_token,
            verification_token_expires=verification_expires,
            is_verified=False,
            is_active=True
        )
        
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        
        # Send verification email
        try:
            self.email_service.send_verification_email(
                to_email=new_user.email,
                name=new_user.name,
                verification_token=verification_token
            )
        except Exception as e:
            print(f"Error sending verification email: {e}")
            # Don't fail registration if email fails
        
        user_response = UserResponse.from_orm(new_user)
        return user_response, "User registered successfully. Please check your email for verification."
    
    def signin(self, credentials: UserSignin) -> AuthResponse:
        """
        Sign in a user
        
        Args:
            credentials: User login credentials
            
        Returns:
            Authentication response with token
            
        Raises:
            AuthenticationError: If authentication fails
        """
        # Find user by email
        user = self.db.query(User).filter(User.email == credentials.email).first()
        if not user:
            raise AuthenticationError("Invalid email or password")
        
        # Check password
        if not self.password_handler.verify_password(credentials.password, user.password_hash):
            raise AuthenticationError("Invalid email or password")
        
        # Check if account is active
        if not user.is_active:
            raise AuthenticationError("Account is disabled")
        
        # Check if email is verified
        if not user.is_verified:
            raise AuthenticationError("Please verify your email before signing in")
        
        # Update last login
        user.last_login = datetime.utcnow()
        self.db.commit()
        
        # Generate access token
        token_data = {
            "sub": user.id,
            "email": user.email,
            "name": user.name
        }
        access_token = self.jwt_handler.create_access_token(token_data)
        
        user_response = UserResponse.from_orm(user)
        
        return AuthResponse(
            message="Sign in successful",
            user=user_response,
            access_token=access_token,
            token_type="bearer",
            expires_in=1800  # 30 minutes
        )
    
    def verify_email(self, token: str) -> EmailVerificationResponse:
        """
        Verify user email with token
        
        Args:
            token: Email verification token
            
        Returns:
            Email verification response
            
        Raises:
            ValidationError: If verification fails
        """
        # Find user by verification token
        user = self.db.query(User).filter(
            and_(
                User.verification_token == token,
                User.verification_token_expires > datetime.utcnow()
            )
        ).first()
        
        if not user:
            raise ValidationError("Invalid or expired verification token")
        
        # Mark user as verified
        user.is_verified = True
        user.verification_token = None
        user.verification_token_expires = None
        user.last_login = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(user)
        
        # Send welcome email
        try:
            self.email_service.send_welcome_email(
                to_email=user.email,
                name=user.name
            )
        except Exception as e:
            print(f"Error sending welcome email: {e}")
        
        # Generate access token for automatic signin
        token_data = {
            "sub": user.id,
            "email": user.email,
            "name": user.name
        }
        access_token = self.jwt_handler.create_access_token(token_data)
        
        return EmailVerificationResponse(
            message="Email verified successfully. You are now signed in.",
            is_verified=True,
            access_token=access_token,
            token_type="bearer",
            expires_in=1800  # 30 minutes
        )
    
    def resend_verification_email(self, email: str) -> str:
        """
        Resend verification email
        
        Args:
            email: User email address
            
        Returns:
            Success message
            
        Raises:
            ValidationError: If user not found or already verified
        """
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            raise ValidationError("User not found")
        
        if user.is_verified:
            raise ValidationError("Email already verified")
        
        # Generate new verification token
        verification_token = self.password_handler.generate_secure_token(32)
        verification_expires = datetime.utcnow() + timedelta(hours=24)
        
        user.verification_token = verification_token
        user.verification_token_expires = verification_expires
        
        self.db.commit()
        
        # Send verification email
        try:
            self.email_service.send_verification_email(
                to_email=user.email,
                name=user.name,
                verification_token=verification_token
            )
        except Exception as e:
            print(f"Error sending verification email: {e}")
            raise ValidationError("Failed to send verification email")
        
        return "Verification email sent successfully"
    
    def request_password_reset(self, email: str) -> str:
        """
        Request password reset
        
        Args:
            email: User email address
            
        Returns:
            Success message
            
        Raises:
            ValidationError: If user not found
        """
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            raise ValidationError("User not found")
        
        # Generate reset token
        reset_token = self.password_handler.generate_secure_token(32)
        reset_expires = datetime.utcnow() + timedelta(hours=1)
        
        user.reset_token = reset_token
        user.reset_token_expires = reset_expires
        
        self.db.commit()
        
        # Send reset email
        try:
            self.email_service.send_password_reset_email(
                to_email=user.email,
                name=user.name,
                reset_token=reset_token
            )
        except Exception as e:
            print(f"Error sending reset email: {e}")
            raise ValidationError("Failed to send reset email")
        
        return "Password reset email sent successfully"
    
    def reset_password(self, token: str, new_password: str) -> str:
        """
        Reset user password
        
        Args:
            token: Password reset token
            new_password: New password
            
        Returns:
            Success message
            
        Raises:
            ValidationError: If reset fails
        """
        # Find user by reset token
        user = self.db.query(User).filter(
            and_(
                User.reset_token == token,
                User.reset_token_expires > datetime.utcnow()
            )
        ).first()
        
        if not user:
            raise ValidationError("Invalid or expired reset token")
        
        # Validate new password
        is_strong, message = self.password_handler.is_password_strong(new_password)
        if not is_strong:
            raise ValidationError(message)
        
        # Hash new password
        password_hash = self.password_handler.hash_password(new_password)
        
        # Update user
        user.password_hash = password_hash
        user.reset_token = None
        user.reset_token_expires = None
        
        self.db.commit()
        
        return "Password reset successfully"
    
    def get_current_user(self, token: str) -> Optional[User]:
        """
        Get current user from token
        
        Args:
            token: JWT access token
            
        Returns:
            User object or None if invalid
        """
        token_data = self.jwt_handler.decode_token(token)
        if not token_data:
            return None
        
        user = self.db.query(User).filter(User.id == token_data.user_id).first()
        return user
    
    def refresh_token(self, refresh_token: str) -> AuthResponse:
        """
        Refresh access token
        
        Args:
            refresh_token: JWT refresh token
            
        Returns:
            New authentication response
            
        Raises:
            AuthenticationError: If refresh fails
        """
        # Verify refresh token
        payload = self.jwt_handler.verify_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise AuthenticationError("Invalid refresh token")
        
        # Get user
        user_id = payload.get("sub")
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user or not user.is_active:
            raise AuthenticationError("User not found or inactive")
        
        # Generate new access token
        token_data = {
            "sub": user.id,
            "email": user.email,
            "name": user.name
        }
        access_token = self.jwt_handler.create_access_token(token_data)
        
        user_response = UserResponse.from_orm(user)
        
        return AuthResponse(
            message="Token refreshed successfully",
            user=user_response,
            access_token=access_token,
            token_type="bearer",
            expires_in=1800  # 30 minutes
        ) 