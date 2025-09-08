#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
django.setup()

from django.test import Client
from django.urls import reverse

def test_login_page_logo():
    print("Testing login page logo rendering...")
    
    client = Client()
    
    try:
        # Get the login page
        response = client.get(reverse('fbc_users:login'))
        print(f"Login page status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            # Check if system_logo is in the context
            if 'system_logo' in str(response.context):
                system_logo = response.context.get('system_logo')
                print(f"✅ system_logo in context: {system_logo}")
            else:
                print("❌ system_logo not found in context")
            
            # Check if logo URL appears in HTML
            if '/media/system/FBC-small-1-150x150' in content:
                print("✅ Logo URL found in rendered HTML")
                
                # Find the img tags with the logo
                import re
                img_matches = re.findall(r'<img[^>]*src="[^"]*FBC-small-1-150x150[^"]*"[^>]*>', content)
                print(f"✅ Found {len(img_matches)} img tags with logo:")
                for i, match in enumerate(img_matches, 1):
                    print(f"   {i}. {match}")
            else:
                print("❌ Logo URL not found in rendered HTML")
                
            # Check for system_name
            if 'FBC Library System' in content:
                print("✅ System name found in rendered HTML")
            else:
                print("❌ System name not found in rendered HTML")
                
        else:
            print(f"❌ Failed to load login page: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing login page: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_login_page_logo()
