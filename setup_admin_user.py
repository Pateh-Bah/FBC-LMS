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

from fbc_users.models import CustomUser

# Create or update admin user with known password
username = 'admin'
password = 'admin123'

try:
    # Try to get existing admin user
    admin_user = CustomUser.objects.get(username=username)
    # Set password
    admin_user.set_password(password)
    admin_user.save()
    print(f"✅ Updated password for existing admin user: {username}")
except CustomUser.DoesNotExist:
    # Create new admin user
    admin_user = CustomUser.objects.create_user(
        username=username,
        email='admin@example.com',
        password=password,
        user_type='admin',
        first_name='Admin',
        last_name='User'
    )
    print(f"✅ Created new admin user: {username}")

print(f"Username: {username}")
print(f"Password: {password}")
print(f"User Type: {admin_user.user_type}")
print(f"Is Active: {admin_user.is_active}")
print(f"Is Staff: {admin_user.is_staff}")

print("\n🔧 To test the add user page:")
print("1. Go to http://127.0.0.1:8000/users/login/")
print(f"2. Login with username: {username} and password: {password}")
print("3. Navigate to http://127.0.0.1:8000/users/manage-users/add/")
print("4. You should now be able to access the add user page!")