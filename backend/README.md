# 🎳 Bowling Replay System - Backend API

AI-Powered Bowling Replay System with Computer Vision, User Management, and Email Verification.

## 📋 Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Authentication Flow](#authentication-flow)
- [API Endpoints](#api-endpoints)
- [Setup Instructions](#setup-instructions)
- [Email Configuration](#email-configuration)
- [Testing](#testing)
- [Architecture](#architecture)
- [Database Schema](#database-schema)
- [Environment Variables](#environment-variables)

## ✨ Features

### 🔐 **User Authentication System**
- **Secure User Registration** with email verification
- **JWT-based Authentication** with access and refresh tokens
- **Password Security** with bcrypt hashing and strength validation
- **Email Verification** flow with resend capability
- **Password Reset** functionality via email
- **Account Management** with user profiles

### 📧 **Email System**
- Beautiful HTML email templates
- Email verification with 24-hour expiry
- Password reset emails with 1-hour expiry
- Welcome emails after verification
- SMTP integration (Gmail, SendGrid, etc.)

### 🛡️ **Security Features**
- Strong password validation (8+ chars, uppercase, lowercase, number)
- JWT token expiration and refresh
- Rate limiting protection
- CORS configuration
- Input validation with Pydantic
- SQL injection prevention with SQLAlchemy

## 🚀 Quick Start

### 1. **Install Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

### 2. **Run the Server**
```bash
python main.py
```

### 3. **Test the API**
```bash
python test_auth_example.py
```

### 4. **Access API Documentation**
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔄 Authentication Flow

Based on your signup screen image, here's the complete authentication flow:

### 📱 **Signup Flow**
1. **User fills signup form**:
   - Email Address
   - Name
   - Password (with strength validation)

2. **System creates account**:
   - Validates email uniqueness
   - Hashes password with bcrypt
   - Generates verification token
   - Sends verification email

3. **Email verification**:
   - User receives email with verification link
   - Clicks link to verify email
   - **Automatically signed in** after verification

4. **Future logins**:
   - User signs in with email/password
   - Receives JWT access token
   - Can access protected resources

### 🔐 **Signin Flow**
1. **User enters credentials**
2. **System validates**:
   - Email exists
   - Password is correct
   - Account is verified and active
3. **Returns JWT token** for authenticated requests

## 🛤️ API Endpoints

### **Authentication (`/api/v1/auth`)**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/signup` | POST | Register new user |
| `/signin` | POST | Sign in user |
| `/verify-email` | POST | Verify email with token |
| `/resend-verification` | POST | Resend verification email |
| `/forgot-password` | POST | Request password reset |
| `/reset-password` | POST | Reset password with token |
| `/refresh-token` | POST | Refresh access token |
| `/me` | GET | Get current user info |
| `/health` | GET | Health check |

### **Example API Calls**

#### **Signup**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "name": "John Doe",
    "password": "SecurePassword123"
  }'
```

#### **Signin**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/signin" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePassword123"
  }'
```

#### **Get User Profile**
```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## ⚙️ Setup Instructions

### **1. Database Setup**
The system uses SQLite by default (no additional setup required):
```python
# Database file will be created automatically at:
./bowling_replay.db
```

### **2. Environment Configuration**
Create a `.env` file in the backend directory:
```env
# Email Configuration (Required for email verification)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=noreply@bowlingreplay.com

# JWT Security (Change in production!)
SECRET_KEY=your-super-secret-jwt-key-here

# Application URLs
BASE_URL=http://localhost:3000
API_BASE_URL=http://localhost:8000
```

### **3. Install System Dependencies**
```bash
# For video processing (optional for auth testing)
# Windows: Download FFmpeg and add to PATH
# Mac: brew install ffmpeg
# Linux: sudo apt-get install ffmpeg
```

## 📧 Email Configuration

### **Gmail Setup**
1. **Enable 2-Factor Authentication** in your Google account
2. **Generate App Password**:
   - Go to Google Account Settings → Security
   - Select "App passwords"
   - Generate password for "Mail"
3. **Use in environment**:
   ```env
   SMTP_USERNAME=your-email@gmail.com
   SMTP_PASSWORD=your-16-char-app-password
   ```

### **Email Templates**
The system includes beautiful HTML email templates:
- ✅ **Verification Email** - Welcome message with verification button
- 🔄 **Password Reset** - Secure reset link with expiry
- 🎉 **Welcome Email** - Sent after successful verification

## 🧪 Testing

### **Run Test Suite**
```bash
python test_auth_example.py
```

### **Manual Testing**
1. **Start the server**: `python main.py`
2. **Open browser**: http://localhost:8000/docs
3. **Test signup flow** in Swagger UI
4. **Check email** for verification link
5. **Test signin** after verification

### **Database Inspection**
```python
# View users in SQLite
import sqlite3
conn = sqlite3.connect('bowling_replay.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
print(cursor.fetchall())
```

## 🏗️ Architecture

### **Project Structure**
```
backend/
├── main.py                 # FastAPI application
├── requirements.txt        # Dependencies
├── test_auth_example.py    # Test suite
│
├── config/                 # Configuration
│   ├── database.py         # SQLAlchemy setup
│   ├── settings.py         # Environment settings
│   └── redis.py           # Redis configuration
│
├── database/              # Database layer
│   ├── models/           # SQLAlchemy models
│   │   └── user.py       # User model
│   ├── schemas/          # Pydantic schemas
│   │   └── user.py       # User validation schemas
│   └── operations/       # Database operations
│       └── user.py       # User CRUD operations
│
├── auth/                  # Authentication
│   ├── jwt_handler.py     # JWT token management
│   ├── password_handler.py # Password hashing
│   └── dependencies.py   # FastAPI auth dependencies
│
├── services/              # Business logic
│   ├── auth_service.py    # Authentication service
│   └── email_service.py   # Email sending service
│
├── api/                   # API endpoints
│   └── v1/endpoints/
│       └── auth.py        # Authentication routes
│
├── utils/                 # Utilities
│   └── exceptions.py      # Custom exceptions
│
└── cv/                    # Computer vision (for future)
    ├── detection/         # Event detection
    ├── processing/        # Video processing
    └── pipeline/          # CV pipeline
```

### **Technology Stack**
- **FastAPI** - High-performance async web framework
- **SQLAlchemy** - Database ORM with SQLite
- **Pydantic** - Data validation and settings
- **JWT** - Secure token-based authentication
- **bcrypt** - Password hashing
- **SMTP** - Email delivery
- **Jinja2** - Email templates

## 🗄️ Database Schema

### **Users Table**
```sql
CREATE TABLE users (
    id VARCHAR PRIMARY KEY,           -- UUID
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    
    -- Email verification
    is_verified BOOLEAN DEFAULT FALSE,
    verification_token VARCHAR(255),
    verification_token_expires DATETIME,
    
    -- Account status
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Password reset
    reset_token VARCHAR(255),
    reset_token_expires DATETIME,
    
    -- Timestamps
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME,
    
    -- Optional profile
    phone VARCHAR(20),
    avatar_url VARCHAR(500)
);
```

## 🌍 Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | Database connection string | `sqlite:///./bowling_replay.db` | No |
| `SECRET_KEY` | JWT secret key | `your-super-secret-jwt-key-here` | **Yes** |
| `SMTP_USERNAME` | Email username | `your-email@gmail.com` | **Yes** |
| `SMTP_PASSWORD` | Email password/app password | `your-app-password` | **Yes** |
| `BASE_URL` | Frontend URL | `http://localhost:3000` | No |
| `DEBUG` | Development mode | `true` | No |

## 🚀 Production Deployment

### **Environment Setup**
```env
# Production environment
ENVIRONMENT=production
DEBUG=false

# Secure JWT key (generate new one!)
SECRET_KEY=your-production-secret-key-256-bits

# Production database
DATABASE_URL=postgresql://user:pass@host:port/db

# Email service
SMTP_SERVER=smtp.sendgrid.net
SMTP_USERNAME=apikey
SMTP_PASSWORD=your-sendgrid-api-key

# Production URLs
BASE_URL=https://your-domain.com
API_BASE_URL=https://api.your-domain.com

# Security
CORS_ORIGINS=https://your-domain.com
ALLOWED_HOSTS=your-domain.com,api.your-domain.com
```

### **Docker Deployment**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📞 Support

For questions or issues:
1. **Check the logs** for error details
2. **Verify email configuration** if emails aren't sending
3. **Test with provided test suite**
4. **Review API documentation** at `/docs`

## 🎯 Next Steps

1. **Configure email provider** (Gmail/SendGrid)
2. **Test complete signup flow**
3. **Integrate with frontend**
4. **Add password reset flow**
5. **Set up production deployment**
6. **Implement computer vision features**

---

**Built with ❤️ for the Bowling Replay System** 