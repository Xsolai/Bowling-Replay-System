from sqlalchemy import Column, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from config.database import Base
import uuid

class User(Base):
    __tablename__ = "users"
    
    # Primary key
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Basic user information
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    
    # Email verification fields
    is_verified = Column(Boolean, default=False, nullable=False)
    verification_token = Column(String(255), unique=True, nullable=True)
    verification_token_expires = Column(DateTime, nullable=True)
    
    # Account status
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Password reset fields
    reset_token = Column(String(255), unique=True, nullable=True)
    reset_token_expires = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    last_login = Column(DateTime, nullable=True)
    
    # Optional profile fields
    phone = Column(String(20), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, name={self.name})>"
    
    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "is_verified": self.is_verified,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "phone": self.phone,
            "avatar_url": self.avatar_url
        } 