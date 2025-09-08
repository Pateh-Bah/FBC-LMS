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

from django.http import HttpRequest
from fbc_users.views import add_user
from fbc_users.models import CustomUser

# Get a test admin user
admin_user = CustomUser.objects.filter(user_type='admin').first()

if admin_user:
    print(f"Testing with admin user: {admin_user.username}")
    
    # Create a mock request
    request = HttpRequest()
    request.method = 'GET'
    request.user = admin_user
    
    try:
        # Call the view directly
        response = add_user(request)
        print(f"✅ View executed successfully!")
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            if "Add New Library Member" in content:
                print("✅ Template renders correctly - contains expected title")
            else:
                print("⚠️ Template may have issues - title not found")
                
            # Check for any obvious template errors
            if "TemplateSyntaxError" in content:
                print("❌ Template syntax error detected")
            elif "TemplateDoesNotExist" in content:
                print("❌ Template does not exist error")
            else:
                print("✅ No obvious template errors detected")
                
        else:
            print(f"❌ Non-200 response: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception in view: {str(e)}")
        import traceback
        traceback.print_exc()
        
else:
    print("❌ No admin user found for testing")