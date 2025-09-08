#!/usr/bin/env python
"""
Test script to verify the logout alert fix
"""
import os
import sys
import django
from django.conf import settings

# Add the project directory to Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_dir)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.urls import reverse

class LogoutAlertTest:
    def __init__(self):
        self.client = Client()
        self.User = get_user_model()
        
    def test_logout_consistency(self):
        """Test that all logout links use the same URL"""
        print("Testing logout URL consistency...")
        
        # Create and login a test user
        try:
            user = self.User.objects.create_user(
                username='testuser', 
                password='testpass123',
                email='test@example.com',
                user_type='student'
            )
            
            # Login
            login_success = self.client.login(username='testuser', password='testpass123')
            if login_success:
                print("✅ User logged in successfully")
                
                # Test logout
                response = self.client.post('/users/logout/')
                if response.status_code == 302:  # Should redirect to login
                    print("✅ Logout redirects correctly")
                    
                    # Check that we're redirected to login page
                    login_response = self.client.get('/users/login/')
                    if login_response.status_code == 200:
                        print("✅ Login page accessible after logout")
                        
                        # Check messages on login page
                        messages = list(get_messages(login_response.wsgi_request))
                        print(f"Messages on login page after logout: {len(messages)}")
                        
                        logout_message_count = 0
                        for message in messages:
                            print(f"  - {message.tags}: {message}")
                            if 'logged out' in str(message).lower() or 'logout' in str(message).lower():
                                logout_message_count += 1
                                
                        if logout_message_count == 1:
                            print("✅ Exactly one logout message displayed")
                        elif logout_message_count == 0:
                            print("⚠️ No logout message displayed")
                        else:
                            print(f"❌ Multiple logout messages: {logout_message_count}")
                            
                    else:
                        print("❌ Login page not accessible after logout")
                else:
                    print(f"❌ Logout returned status: {response.status_code}")
            else:
                print("❌ Login failed")
                
        except Exception as e:
            print(f"❌ Test failed: {e}")
        finally:
            # Cleanup
            try:
                self.User.objects.filter(username='testuser').delete()
                print("✅ Test user cleaned up")
            except:
                pass
    
    def test_template_consistency(self):
        """Test that logout URLs are consistent across templates"""
        print("\nTesting template logout URL consistency...")
        
        import re
        from pathlib import Path
        
        template_dir = Path(project_dir) / 'templates'
        logout_urls = set()
        templates_with_logout = []
        
        # Search for logout URLs in templates
        for template_file in template_dir.rglob('*.html'):
            try:
                content = template_file.read_text(encoding='utf-8')
                logout_matches = re.findall(r"url\s+['\"]([^'\"]*logout[^'\"]*)['\"]", content)
                if logout_matches:
                    for match in logout_matches:
                        logout_urls.add(match)
                        templates_with_logout.append((str(template_file), match))
            except Exception as e:
                print(f"Error reading {template_file}: {e}")
        
        print(f"Found logout URLs: {logout_urls}")
        print(f"Templates with logout links: {len(templates_with_logout)}")
        
        if len(logout_urls) == 1 and 'fbc_users:logout' in logout_urls:
            print("✅ All templates use consistent logout URL: fbc_users:logout")
        else:
            print("❌ Inconsistent logout URLs found:")
            for template, url in templates_with_logout:
                print(f"  {template}: {url}")
    
    def run_tests(self):
        """Run all logout tests"""
        print("=" * 60)
        print("LOGOUT ALERT FIX VERIFICATION")
        print("=" * 60)
        
        self.test_template_consistency()
        self.test_logout_consistency()
        
        print("\n" + "=" * 60)
        print("Tests completed")

if __name__ == '__main__':
    tester = LogoutAlertTest()
    tester.run_tests()
