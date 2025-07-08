import os
from typing import List, Optional
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    """Application settings and configuration"""
    
    # Application
    app_name: str = "Bowling Replay System API"
    app_version: str = "1.0.0"
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=True, env="DEBUG")
    
    # API Configuration
    api_prefix: str = "/api/v1"
    base_url: str = Field(default="http://localhost:3000", env="BASE_URL")
    api_base_url: str = Field(default="http://localhost:8000", env="API_BASE_URL")
    
    # Database
    database_url: str = Field(default="sqlite:///./bowling_replay.db", env="DATABASE_URL")
    
    # JWT Configuration
    secret_key: str = Field(default="your-super-secret-jwt-key-here", env="SECRET_KEY")
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(default=7, env="REFRESH_TOKEN_EXPIRE_DAYS")
    
    # Email Configuration
    smtp_server: str = Field(default="smtp.gmail.com", env="SMTP_SERVER")
    smtp_port: int = Field(default=587, env="SMTP_PORT")
    smtp_username: str = Field(default="your-email@gmail.com", env="SMTP_USERNAME")
    smtp_password: str = Field(default="your-app-password", env="SMTP_PASSWORD")
    from_email: str = Field(default="noreply@bowlingreplay.com", env="FROM_EMAIL")
    from_name: str = Field(default="Bowling Replay System", env="FROM_NAME")
    
    # Redis Configuration
    redis_url: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    
    # Celery Configuration
    celery_broker_url: str = Field(default="redis://localhost:6379/0", env="CELERY_BROKER_URL")
    celery_result_backend: str = Field(default="redis://localhost:6379/0", env="CELERY_RESULT_BACKEND")
    
    # Stripe Configuration
    stripe_publishable_key: str = Field(default="", env="STRIPE_PUBLISHABLE_KEY")
    stripe_secret_key: str = Field(default="", env="STRIPE_SECRET_KEY")
    stripe_webhook_secret: str = Field(default="", env="STRIPE_WEBHOOK_SECRET")
    
    # PayPal Configuration
    paypal_client_id: str = Field(default="", env="PAYPAL_CLIENT_ID")
    paypal_client_secret: str = Field(default="", env="PAYPAL_CLIENT_SECRET")
    paypal_mode: str = Field(default="sandbox", env="PAYPAL_MODE")
    
    # Twilio Configuration
    twilio_account_sid: str = Field(default="", env="TWILIO_ACCOUNT_SID")
    twilio_auth_token: str = Field(default="", env="TWILIO_AUTH_TOKEN")
    twilio_phone_number: str = Field(default="", env="TWILIO_PHONE_NUMBER")
    
    # AWS Configuration
    aws_access_key_id: str = Field(default="", env="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str = Field(default="", env="AWS_SECRET_ACCESS_KEY")
    aws_region: str = Field(default="us-east-1", env="AWS_REGION")
    aws_s3_bucket: str = Field(default="bowling-replay-videos", env="AWS_S3_BUCKET")
    
    # Google Cloud Configuration
    gcp_project: str = Field(default="", env="GOOGLE_CLOUD_PROJECT")
    gcp_bucket: str = Field(default="bowling-replay-gcp", env="GOOGLE_CLOUD_BUCKET")
    gcp_credentials_path: str = Field(default="", env="GOOGLE_APPLICATION_CREDENTIALS")
    
    # Computer Vision Configuration
    cv_model_path: str = Field(default="models/", env="CV_MODEL_PATH")
    yolo_model_path: str = Field(default="models/yolov8n.pt", env="YOLO_MODEL_PATH")
    mediapipe_model_complexity: int = Field(default=2, env="MEDIAPIPE_MODEL_COMPLEXITY")
    detection_confidence_threshold: float = Field(default=0.7, env="DETECTION_CONFIDENCE_THRESHOLD")
    tracking_confidence_threshold: float = Field(default=0.5, env="TRACKING_CONFIDENCE_THRESHOLD")
    
    # Video Processing Configuration
    ffmpeg_executable: str = Field(default="ffmpeg", env="FFMPEG_EXECUTABLE")
    video_quality: str = Field(default="1080p", env="VIDEO_QUALITY")
    video_fps: int = Field(default=30, env="VIDEO_FPS")
    clip_max_duration: int = Field(default=30, env="CLIP_MAX_DURATION")
    
    # Security Configuration
    allowed_hosts: List[str] = Field(default=["localhost", "127.0.0.1"], env="ALLOWED_HOSTS")
    cors_origins: List[str] = Field(default=["http://localhost:3000"], env="CORS_ORIGINS")
    max_upload_size_mb: int = Field(default=100, env="MAX_UPLOAD_SIZE_MB")
    
    # Rate Limiting
    rate_limit_per_minute: int = Field(default=60, env="RATE_LIMIT_PER_MINUTE")
    rate_limit_per_hour: int = Field(default=1000, env="RATE_LIMIT_PER_HOUR")
    
    # Cache Configuration
    cache_ttl_seconds: int = Field(default=300, env="CACHE_TTL_SECONDS")
    cache_max_size_mb: int = Field(default=512, env="CACHE_MAX_SIZE_MB")
    
    # Monitoring and Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    prometheus_port: int = Field(default=9090, env="PROMETHEUS_PORT")
    sentry_dsn: str = Field(default="", env="SENTRY_DSN")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

# Global settings instance
settings = Settings()

# Helper functions
def get_database_url() -> str:
    """Get database URL"""
    return settings.database_url

def get_redis_url() -> str:
    """Get Redis URL"""
    return settings.redis_url

def is_development() -> bool:
    """Check if running in development mode"""
    return settings.environment.lower() == "development"

def is_production() -> bool:
    """Check if running in production mode"""
    return settings.environment.lower() == "production"

def get_cors_origins() -> List[str]:
    """Get CORS origins"""
    if isinstance(settings.cors_origins, str):
        return [origin.strip() for origin in settings.cors_origins.split(",")]
    return settings.cors_origins

def get_allowed_hosts() -> List[str]:
    """Get allowed hosts"""
    if isinstance(settings.allowed_hosts, str):
        return [host.strip() for host in settings.allowed_hosts.split(",")]
    return settings.allowed_hosts 