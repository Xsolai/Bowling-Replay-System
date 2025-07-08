from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
import re

# Base User Schema
class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=2, max_length=100)

# User Registration Schema
class UserSignup(UserBase):
    password: str = Field(..., min_length=8, max_length=100)
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one number')
        return v
    
    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        if len(v.strip()) < 2:
            raise ValueError('Name must be at least 2 characters long')
        return v.strip()

# User Login Schema
class UserSignin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)

# Email Verification Schema
class EmailVerification(BaseModel):
    token: str = Field(..., min_length=1)

# Password Reset Request Schema
class PasswordResetRequest(BaseModel):
    email: EmailStr

# Password Reset Schema
class PasswordReset(BaseModel):
    token: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8, max_length=100)
    
    @validator('new_password')
    def validate_new_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one number')
        return v

# User Response Schema
class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    is_verified: bool
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    
    class Config:
        from_attributes = True

# User Profile Update Schema
class UserProfileUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    phone: Optional[str] = Field(None, regex=r'^\+?1?\d{9,15}$')
    avatar_url: Optional[str] = Field(None, max_length=500)
    
    @validator('name')
    def validate_name(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip() if v else v

# Authentication Token Response Schema
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse

# Authentication Success Response
class AuthResponse(BaseModel):
    message: str
    user: UserResponse
    access_token: str
    token_type: str = "bearer"
    expires_in: int

# Email Verification Success Response
class EmailVerificationResponse(BaseModel):
    message: str
    is_verified: bool
    access_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: Optional[int] = None

# Generic Response Schema
class MessageResponse(BaseModel):
    message: str
    success: bool = True 