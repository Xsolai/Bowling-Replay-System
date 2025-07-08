from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from config.database import create_tables
from api.v1.endpoints import auth
from utils.exceptions import BaseCustomException

# Create FastAPI app
app = FastAPI(
    title="Bowling Replay System API",
    description="AI-Powered Bowling Replay System with Computer Vision",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Authentication",
            "description": "User authentication and authorization endpoints"
        }
    ]
)

# Add security schemes to OpenAPI
from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Bowling Replay System API",
        version="1.0.0",
        description="AI-Powered Bowling Replay System with Computer Vision",
        routes=app.routes,
    )
    
    # Add multiple security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT token authentication (use /api/v1/auth/signin to get token)"
        },
        "HTTPBasic": {
            "type": "http",
            "scheme": "basic",
            "description": "Basic authentication using email and password"
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Startup event
@app.on_event("startup")
async def startup_event():
    print("🚀 Starting Bowling Replay System API...")
    print("📊 Creating database tables...")
    create_tables()
    print("✅ Database tables created successfully")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    print("🛑 Shutting down Bowling Replay System API...")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handler for custom exceptions
@app.exception_handler(BaseCustomException)
async def custom_exception_handler(request: Request, exc: BaseCustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.message,
            "details": exc.details
        }
    )

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": True,
            "message": "An unexpected error occurred",
            "details": {}
        }
    )

# Include routers
app.include_router(
    auth.router, 
    prefix="/api/v1/auth", 
    tags=["Authentication"]
)

# Root endpoint
@app.get("/")
async def root():
    """
    API root endpoint
    """
    return {
        "message": "Welcome to Bowling Replay System API",
        "version": "1.0.0",
        "status": "running",
        "features": [
            "🎳 AI-Powered Bowling Event Detection",
            "📹 Multi-Camera Video Processing", 
            "👤 User Authentication & Management",
            "📧 Email Verification System",
            "💳 Payment Integration",
            "📱 SMS/MMS Notifications"
        ]
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "service": "bowling-replay-api",
        "timestamp": "2024-01-01T00:00:00Z"
    }

# API information endpoint
@app.get("/api/v1/info")
async def api_info():
    """
    API information endpoint
    """
    return {
        "api_name": "Bowling Replay System API",
        "version": "1.0.0",
        "description": "AI-Powered Bowling Replay System with Computer Vision",
        "endpoints": {
            "authentication": "/api/v1/auth",
            "sessions": "/api/v1/sessions",
            "clips": "/api/v1/clips",
            "payments": "/api/v1/payments",
            "cv_events": "/api/v1/cv-events",
            "lanes": "/api/v1/lanes",
            "users": "/api/v1/users"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    ) 