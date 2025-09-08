import os
import sys
import django
import traceback

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
from django.http import Http404

# Create a test client
client = Client()

# Get test user
User = get_user_model()
test_user = User.objects.filter(username='testadmin').first()

if test_user:
    print(f"Using test user: {test_user.username}")
    
    # Login
    login_success = client.login(username='testadmin', password='testpass123')
    print(f"Login success: {login_success}")
    
    if login_success:
        try:
            # Try to access the add user page with more detailed error handling
            response = client.get('/users/manage-users/add/', follow=True)
            print(f"Response status: {response.status_code}")
            print(f"Response URL: {response.request.get('PATH_INFO', 'N/A')}")
            
            if response.status_code == 400:
                # Get response content to see the error
                content = response.content.decode('utf-8')
                print("\n=== Response Content ===")
                if "TemplateSyntaxError" in content:
                    print("❌ Template Syntax Error detected!")
                    # Extract error details
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if "TemplateSyntaxError" in line or "Invalid block tag" in line:
                            print(f"Error: {line.strip()}")
                            # Print surrounding lines for context
                            for j in range(max(0, i-2), min(len(lines), i+3)):
                                print(f"  {j}: {lines[j].strip()}")
                            break
                elif "TemplateDoesNotExist" in content:
                    print("❌ Template Does Not Exist error!")
                    lines = content.split('\n')
                    for line in lines:
                        if "TemplateDoesNotExist" in line:
                            print(f"Error: {line.strip()}")
                            break
                else:
                    print("❌ Other 400 error. First 1000 chars of response:")
                    print(content[:1000])
            elif response.status_code == 200:
                print("✅ Page loads successfully!")
                print("Page title:", response.content.decode('utf-8').split('<title>')[1].split('</title>')[0] if '<title>' in response.content.decode('utf-8') else 'No title found')
            else:
                print(f"❌ Unexpected status code: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Exception occurred: {str(e)}")
            print("Full traceback:")
            traceback.print_exc()
    else:
        print("❌ Login failed")
else:
    print("❌ Test user not found")