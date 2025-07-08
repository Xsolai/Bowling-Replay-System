#!/usr/bin/env python3
"""
Test script to verify the improved signup functionality
"""
import requests
import json

def test_signup_with_unverified_user():
    """Test signup with an existing unverified user"""
    url = "http://localhost:8000/api/v1/auth/signup"
    
    # Test data for existing unverified user
    test_data = {
        "email": "test@xsol.ai",
        "name": "ahsan",
        "password": "XsolAI@123"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=test_data, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 201:
            print("✅ SUCCESS: Signup with unverified user worked - verification email sent")
        else:
            print("❌ FAILED: Unexpected response")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: {e}")

def test_signup_with_new_user():
    """Test signup with a new user"""
    url = "http://localhost:8000/api/v1/auth/signup"
    
    # Test data for new user
    test_data = {
        "email": "newuser@xsol.ai",
        "name": "New User",
        "password": "NewPassword123"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=test_data, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 201:
            print("✅ SUCCESS: Signup with new user worked")
        else:
            print("❌ FAILED: Unexpected response")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    print("Testing improved signup functionality...\n")
    
    print("1. Testing signup with existing unverified user:")
    test_signup_with_unverified_user()
    
    print("\n2. Testing signup with new user:")
    test_signup_with_new_user()
    
    print("\nTest completed!") 