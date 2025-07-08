#!/usr/bin/env python3
"""
Security test to verify authentication properly rejects wrong passwords
"""
import requests
import base64

def test_basic_auth_with_wrong_password():
    """Test that Basic auth rejects wrong passwords"""
    print("Testing Basic Auth with WRONG password...")
    
    # Test with wrong password
    email = "test@xsol.ai"
    wrong_password = "WrongPassword123"
    
    # Create Basic auth header with wrong password
    credentials = f"{email}:{wrong_password}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json"
    }
    
    url = "http://localhost:8000/api/v1/auth/me"
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 401:
            print("✅ SUCCESS: Wrong password properly rejected!")
            return True
        else:
            print("❌ SECURITY ISSUE: Wrong password was accepted!")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_basic_auth_with_correct_password():
    """Test that Basic auth accepts correct passwords"""
    print("\nTesting Basic Auth with CORRECT password...")
    
    # Test with correct password
    email = "test@xsol.ai"
    correct_password = "XsolAI@123"
    
    # Create Basic auth header with correct password
    credentials = f"{email}:{correct_password}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json"
    }
    
    url = "http://localhost:8000/api/v1/auth/me"
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ SUCCESS: Correct password accepted!")
            return True
        else:
            print("❌ FAILED: Correct password was rejected!")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_basic_auth_with_nonexistent_user():
    """Test that Basic auth rejects non-existent users"""
    print("\nTesting Basic Auth with NON-EXISTENT user...")
    
    # Test with non-existent user
    email = "nonexistent@example.com"
    password = "SomePassword123"
    
    # Create Basic auth header
    credentials = f"{email}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json"
    }
    
    url = "http://localhost:8000/api/v1/auth/me"
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 401:
            print("✅ SUCCESS: Non-existent user properly rejected!")
            return True
        else:
            print("❌ SECURITY ISSUE: Non-existent user was accepted!")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    print("Testing authentication security...\n")
    
    # Test wrong password
    wrong_password_test = test_basic_auth_with_wrong_password()
    
    # Test correct password
    correct_password_test = test_basic_auth_with_correct_password()
    
    # Test non-existent user
    nonexistent_user_test = test_basic_auth_with_nonexistent_user()
    
    print(f"\n{'='*60}")
    print("SECURITY TEST RESULTS:")
    print(f"Wrong Password Rejection: {'✅ SECURE' if wrong_password_test else '❌ VULNERABLE'}")
    print(f"Correct Password Acceptance: {'✅ WORKING' if correct_password_test else '❌ BROKEN'}")
    print(f"Non-existent User Rejection: {'✅ SECURE' if nonexistent_user_test else '❌ VULNERABLE'}")
    print(f"{'='*60}")
    
    if all([wrong_password_test, correct_password_test, nonexistent_user_test]):
        print("🔒 Authentication security is working correctly!")
    else:
        print("🚨 SECURITY ISSUES DETECTED! Please fix before using in production.") 