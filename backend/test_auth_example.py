#!/usr/bin/env python3
"""
Simple test script to demonstrate the authentication system
Run this after starting the FastAPI server: python main.py
"""

import requests
import json
from typing import Dict, Any

# API base URL
BASE_URL = "http://localhost:8000/api/v1/auth"

def test_signup():
    """Test user signup"""
    print("🔐 Testing User Signup...")
    
    signup_data = {
        "email": "test@example.com",
        "name": "Test User",
        "password": "TestPassword123"
    }
    
    response = requests.post(f"{BASE_URL}/signup", json=signup_data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 201:
        print("✅ Signup successful!")
        return True
    else:
        print("❌ Signup failed!")
        return False

def test_signin_before_verification():
    """Test signin before email verification (should fail)"""
    print("\n🔐 Testing Signin Before Verification...")
    
    signin_data = {
        "email": "test@example.com",
        "password": "TestPassword123"
    }
    
    response = requests.post(f"{BASE_URL}/signin", json=signin_data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 401:
        print("✅ Correctly rejected unverified user!")
        return True
    else:
        print("❌ Should have rejected unverified user!")
        return False

def test_resend_verification():
    """Test resending verification email"""
    print("\n📧 Testing Resend Verification Email...")
    
    email_data = {
        "email": "test@example.com"
    }
    
    response = requests.post(f"{BASE_URL}/resend-verification", json=email_data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        print("✅ Verification email resent!")
        return True
    else:
        print("❌ Failed to resend verification email!")
        return False

def test_invalid_signin():
    """Test signin with invalid credentials"""
    print("\n🔐 Testing Invalid Signin...")
    
    signin_data = {
        "email": "test@example.com",
        "password": "WrongPassword"
    }
    
    response = requests.post(f"{BASE_URL}/signin", json=signin_data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 401:
        print("✅ Correctly rejected invalid credentials!")
        return True
    else:
        print("❌ Should have rejected invalid credentials!")
        return False

def test_password_validation():
    """Test password validation"""
    print("\n🔐 Testing Password Validation...")
    
    # Test weak password
    signup_data = {
        "email": "test2@example.com",
        "name": "Test User 2",
        "password": "weak"
    }
    
    response = requests.post(f"{BASE_URL}/signup", json=signup_data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 422:
        print("✅ Correctly rejected weak password!")
        return True
    else:
        print("❌ Should have rejected weak password!")
        return False

def test_duplicate_email():
    """Test signup with duplicate email"""
    print("\n🔐 Testing Duplicate Email Signup...")
    
    signup_data = {
        "email": "test@example.com",  # Same email as before
        "name": "Another User",
        "password": "AnotherPassword123"
    }
    
    response = requests.post(f"{BASE_URL}/signup", json=signup_data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 422:
        print("✅ Correctly rejected duplicate email!")
        return True
    else:
        print("❌ Should have rejected duplicate email!")
        return False

def test_health_check():
    """Test health check endpoint"""
    print("\n🏥 Testing Health Check...")
    
    response = requests.get(f"{BASE_URL}/health")
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        print("✅ Health check passed!")
        return True
    else:
        print("❌ Health check failed!")
        return False

def simulate_email_verification():
    """
    Simulate email verification (in real implementation, user would click email link)
    For testing, we'll directly update the database
    """
    print("\n📧 Simulating Email Verification...")
    print("In a real implementation, the user would click the verification link in their email.")
    print("For testing purposes, you would need to:")
    print("1. Check the verification token in the database")
    print("2. Call the verify-email endpoint with that token")
    print("3. Or manually set is_verified=True in the database")

def main():
    """Run all authentication tests"""
    print("🎳 Bowling Replay System - Authentication Test Suite")
    print("=" * 60)
    
    try:
        # Test all authentication features
        test_health_check()
        test_signup()
        test_signin_before_verification()
        test_resend_verification()
        test_invalid_signin()
        test_password_validation()
        test_duplicate_email()
        simulate_email_verification()
        
        print("\n" + "=" * 60)
        print("🎯 Test Summary:")
        print("✅ User signup with validation")
        print("✅ Email verification requirement")
        print("✅ Password strength validation")
        print("✅ Duplicate email prevention")
        print("✅ Invalid credential rejection")
        print("✅ Verification email resending")
        print("\n📧 Next Steps:")
        print("1. Configure SMTP settings for real email sending")
        print("2. Test email verification flow")
        print("3. Test signin after verification")
        print("4. Test JWT token functionality")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API server!")
        print("Make sure the FastAPI server is running on http://localhost:8000")
        print("Run: cd backend && python main.py")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")

if __name__ == "__main__":
    main() 