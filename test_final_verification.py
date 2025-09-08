#!/usr/bin/env python
"""
Final verification script for Django FBC Library System
Run this after starting the Django server to verify everything works
"""

import requests
from urllib.parse import urljoin

# Configuration
BASE_URL = "http://127.0.0.1:8000"
ADMIN_CREDENTIALS = {"username": "fbcadmin", "password": "admin123"}
STAFF_CREDENTIALS = {"username": "fbcstaff", "password": "staff123"}

def test_url_accessibility(session, url, description):
    """Test if a URL is accessible"""
    try:
        response = session.get(url)
        if response.status_code == 200:
            print(f"✅ {description}: {url} (Status: {response.status_code})")
            return True
        else:
            print(f"⚠️  {description}: {url} (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ {description}: {url} (Error: {e})")
        return False

def test_login_and_dashboard(credentials, user_type):
    """Test login and dashboard access for a user"""
    print(f"\n{'='*60}")
    print(f"TESTING {user_type.upper()} USER AUTHENTICATION & DASHBOARD")
    print(f"{'='*60}")
    
    session = requests.Session()
    
    # Get login page to get CSRF token
    login_url = urljoin(BASE_URL, "/users/login/")
    try:
        login_page = session.get(login_url)
        if login_page.status_code != 200:
            print(f"❌ Cannot access login page: {login_page.status_code}")
            return False
            
        # Extract CSRF token
        csrf_token = None
        if 'csrftoken' in session.cookies:
            csrf_token = session.cookies['csrftoken']
        
        print(f"✅ Login page accessible: {login_url}")
        
        # Attempt login
        login_data = {
            'username': credentials['username'],
            'password': credentials['password'],
            'csrfmiddlewaretoken': csrf_token
        }
        
        login_response = session.post(login_url, data=login_data)
        
        if login_response.status_code == 302:  # Redirect after successful login
            print(f"✅ Login successful for {credentials['username']}")
            redirect_url = login_response.headers.get('Location', 'Unknown')
            print(f"   Redirected to: {redirect_url}")
            
            # Test dashboard access based on user type
            if user_type == "admin":
                dashboard_urls = [
                    ("/dashboard/admin/", "Admin Dashboard"),
                    ("/admin/", "Django Admin"),
                    ("/payments/history/", "Payment History"),
                    ("/fines/manage/", "Manage Fines")
                ]
            elif user_type == "staff":
                dashboard_urls = [
                    ("/dashboard/staff/", "Staff Dashboard"),
                    ("/dashboard/", "Main Dashboard")
                ]
            else:
                dashboard_urls = [("/dashboard/", "User Dashboard")]
            
            # Test each dashboard URL
            for path, description in dashboard_urls:
                url = urljoin(BASE_URL, path)
                test_url_accessibility(session, url, description)
                
        else:
            print(f"❌ Login failed for {credentials['username']}: {login_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error during {user_type} login test: {e}")
        return False
    
    return True

def test_public_urls():
    """Test public URLs that should be accessible without login"""
    print(f"\n{'='*60}")
    print("TESTING PUBLIC URL ACCESSIBILITY")
    print(f"{'='*60}")
    
    session = requests.Session()
    public_urls = [
        ("/", "Home Page"),
        ("/users/login/", "Login Page"),
        ("/admin/", "Django Admin Login")
    ]
    
    for path, description in public_urls:
        url = urljoin(BASE_URL, path)
        test_url_accessibility(session, url, description)

def main():
    """Main test function"""
    print("Django FBC Library System - Final Verification Test")
    print("="*70)
    print("\n🔧 PREREQUISITES:")
    print("1. Django server should be running on http://127.0.0.1:8000")
    print("2. Database should contain fbcadmin and fbcstaff users")
    print("3. All migrations should be applied")
    print("\n🚀 Starting tests...\n")
    
    try:
        # Test if server is running
        response = requests.get(BASE_URL, timeout=5)
        print(f"✅ Django server is running: {BASE_URL}")
    except Exception as e:
        print(f"❌ Django server is not accessible: {e}")
        print("\nPlease start the Django server with:")
        print("python manage.py runserver")
        return
    
    # Test public URLs
    test_public_urls()
    
    # Test admin user
    test_login_and_dashboard(ADMIN_CREDENTIALS, "admin")
    
    # Test staff user  
    test_login_and_dashboard(STAFF_CREDENTIALS, "staff")
    
    print(f"\n{'='*60}")
    print("VERIFICATION COMPLETE")
    print(f"{'='*60}")
    print("\n📋 SUMMARY:")
    print("- If you see ✅ for most tests, the system is working correctly")
    print("- ⚠️  warnings indicate the URL is redirecting (may be normal)")
    print("- ❌ errors indicate issues that need to be addressed")
    print("\n🎯 KEY SUCCESS INDICATORS:")
    print("1. Login successful for both fbcadmin and fbcstaff")
    print("2. Admin dashboard accessible after admin login")
    print("3. Payment history and manage fines URLs work")
    print("4. No 500 Internal Server Errors")

if __name__ == "__main__":
    main()
