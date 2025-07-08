from typing import Any, Dict, Optional

class BaseCustomException(Exception):
    """Base exception class for custom exceptions"""
    
    def __init__(self, message: str, status_code: int = 400, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

class ValidationError(BaseCustomException):
    """Raised when validation fails"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=422, details=details)

class AuthenticationError(BaseCustomException):
    """Raised when authentication fails"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=401, details=details)

class AuthorizationError(BaseCustomException):
    """Raised when authorization fails"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=403, details=details)

class NotFoundError(BaseCustomException):
    """Raised when resource is not found"""
    
    def __init__(self, message: str = "Resource not found", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=404, details=details)

class ConflictError(BaseCustomException):
    """Raised when there's a conflict"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=409, details=details)

class RateLimitError(BaseCustomException):
    """Raised when rate limit is exceeded"""
    
    def __init__(self, message: str = "Rate limit exceeded", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=429, details=details)

class InternalServerError(BaseCustomException):
    """Raised for internal server errors"""
    
    def __init__(self, message: str = "Internal server error", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=500, details=details)

class DatabaseError(BaseCustomException):
    """Raised when database operation fails"""
    
    def __init__(self, message: str = "Database operation failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=500, details=details)

class EmailServiceError(BaseCustomException):
    """Raised when email service fails"""
    
    def __init__(self, message: str = "Email service error", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=500, details=details)

class FileUploadError(BaseCustomException):
    """Raised when file upload fails"""
    
    def __init__(self, message: str = "File upload failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=400, details=details)

class CVProcessingError(BaseCustomException):
    """Raised when computer vision processing fails"""
    
    def __init__(self, message: str = "CV processing failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=500, details=details)

class PaymentError(BaseCustomException):
    """Raised when payment processing fails"""
    
    def __init__(self, message: str = "Payment processing failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=400, details=details) 