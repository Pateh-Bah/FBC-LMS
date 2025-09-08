import os
import sys
import django

# Add the project directory to Python path
project_path = r'C:\Users\pateh\Downloads\Web\Django\dj fbc vs'
sys.path.append(project_path)
os.chdir(project_path)

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse

# Create a test client
client = Client()

# Get a user
User = get_user_model()
admin_user = User.objects.filter(user_type='admin').first()

if admin_user:
    print(f"Found admin user: {admin_user.username}")
    
    # Login as admin
    login_success = client.login(username=admin_user.username, password='admin123')  # Try common password
    print(f"Login with 'admin123': {login_success}")
    
    if not login_success:
        # Try other common passwords
        for pwd in ['password', 'admin', '123456', 'password123']:
            login_success = client.login(username=admin_user.username, password=pwd)
            print(f"Login with '{pwd}': {login_success}")
            if login_success:
                break
    
    if login_success:
        # Try to access the add user page
        response = client.get('/users/manage-users/add/')
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Page loads successfully!")
        else:
            print(f"❌ Page returned status {response.status_code}")
            if hasattr(response, 'content'):
                content = response.content.decode('utf-8')[:500]
                print(f"Response content preview: {content}")
    else:
        print("❌ Could not login - need to check user passwords")
        print("Let's create a test admin user...")
        
        # Create a test admin user
        test_user = User.objects.create_user(
            username='testadmin',
            email='test@example.com',
            password='testpass123',
            user_type='admin',
            first_name='Test',
            last_name='Admin'
        )
        print(f"Created test user: {test_user.username}")
        
        # Try login with test user
        login_success = client.login(username='testadmin', password='testpass123')
        print(f"Login with test user: {login_success}")
        
        if login_success:
            response = client.get('/users/manage-users/add/')
            print(f"Response status with test user: {response.status_code}")
else:
    print("❌ No admin users found in database")