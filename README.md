# Bowling-Replay-System
AI-Powered Bowling Replay System 


Main Architecture Components
1. Core Application (main.py, requirements.txt)
FastAPI application entry point
Complete dependency management
2. API Layer (api/)
v1 API endpoints for all major features:
auth.py - Authentication & token management
sessions.py - Bowling session management
clips.py - Video clip access & streaming
payments.py - Stripe/PayPal integration
cv_events.py - Real-time CV event streaming
lanes.py - Lane management & QR codes
users.py - User profile management
websocket.py - Real-time communication
3. Database Layer (database/)
Models: SQLAlchemy models for all entities
Schemas: Pydantic schemas for validation
Operations: CRUD operations with optimized queries
Complete separation of concerns
4. Computer Vision System (cv/)
Detection: Pose estimation, object detection, ball tracking
Processing: Camera management, frame sync, ROI handling
Pipeline: Complete CV pipeline orchestration
Models: YOLO & MediaPipe configuration
5. Services Layer (services/)
Business Logic: All core functionality
External Integrations: Payment, SMS, storage services
Clean Architecture: Separation from API and data layers
6. Background Processing (background/)
Celery Integration: Distributed task processing
Video Tasks: FFmpeg operations, clip generation
CV Tasks: Real-time event processing
Notification Tasks: SMS/MMS delivery
7. Authentication & Security (auth/)
JWT Management: Token generation & validation
Password Security: Hashing & verification
Permissions: Role-based access control
Middleware: Request authentication
8. External Integrations (external/)
Payment Gateways: Stripe, PayPal clients
Cloud Services: AWS, GCP integration
Messaging: Twilio SMS/MMS client
9. Utilities (utils/)
Video Processing: FFmpeg utilities
Security: Encryption & hashing
Caching: Redis management
File Handling: Upload/download operations
QR Generation: Lane assignment codes
10. Monitoring & Health (monitoring/)
Metrics Collection: Performance monitoring
Health Checks: System availability
Alerting: Critical event notifications
11. Deployment (deployment/)
Docker: Complete containerization
Kubernetes: Production orchestration
Nginx: Reverse proxy configuration
12. Testing (tests/)
Comprehensive Test Suite: All major components
Pytest Configuration: Testing framework setup
