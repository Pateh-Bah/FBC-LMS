#!/usr/bin/env python
"""
Test script to verify that subscription alerts only show for students
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

from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class SubscriptionAlertTest:
    def __init__(self):
        self.client = Client()
        self.User = get_user_model()
        
    def test_subscription_alert_visibility(self):
        """Test that subscription alerts only show for students"""
        print("Testing subscription alert visibility by user type...")
        
        # Test different user types
        user_types = ['student', 'lecturer', 'staff', 'admin']
        
        for user_type in user_types:
            print(f"\nTesting {user_type}...")
            
            try:
                # Create user with expired subscription
                user = self.User.objects.create_user(
                    username=f'test_{user_type}',
                    password='testpass123',
                    email=f'{user_type}@example.com',
                    user_type=user_type
                )
                
                # Set subscription as expired (assuming the field exists)
                if hasattr(user, 'subscription_end_date'):
                    from datetime import date, timedelta
                    user.subscription_end_date = date.today() - timedelta(days=30)
                    user.save()
                
                # Login
                login_success = self.client.login(username=f'test_{user_type}', password='testpass123')
                if login_success:
                    print(f"  ✅ {user_type} logged in successfully")
                    
                    # Try to access dashboard
                    response = self.client.get('/dashboard/')
                    if response.status_code == 200:
                        content = response.content.decode('utf-8')
                        
                        # Check for subscription alert
                        subscription_alert_found = 'Your library subscription has expired' in content
                        
                        if user_type == 'student':
                            if subscription_alert_found:
                                print(f"  ✅ {user_type} correctly sees subscription alert")
                            else:
                                print(f"  ⚠️ {user_type} should see subscription alert but doesn't")
                        else:
                            if not subscription_alert_found:
                                print(f"  ✅ {user_type} correctly doesn't see subscription alert")
                            else:
                                print(f"  ❌ {user_type} incorrectly sees subscription alert")
                    else:
                        print(f"  ❌ {user_type} dashboard returned status: {response.status_code}")
                else:
                    print(f"  ❌ {user_type} login failed")
                    
            except Exception as e:
                print(f"  ❌ Test failed for {user_type}: {e}")
            finally:
                # Cleanup
                try:
                    self.User.objects.filter(username=f'test_{user_type}').delete()
                except:
                    pass
    
    def check_template_conditions(self):
        """Check template files for proper user type conditions"""
        print("\nChecking template files for proper subscription alert conditions...")
        
        import re
        from pathlib import Path
        
        template_files = [
            'templates/books/user_dashboard.html',
            'templates/dashboard/user_dashboard.html',
            'templates/dashboard/user_dashboard_base.html',
            'templates/users/student_dashboard.html'
        ]
        
        for template_file in template_files:
            template_path = Path(project_dir) / template_file
            if template_path.exists():
                try:
                    content = template_path.read_text(encoding='utf-8')
                    
                    # Look for subscription-related conditions
                    if 'Your library subscription has expired' in content:
                        # Check if it has proper user type condition
                        if "user.user_type == 'student'" in content:
                            print(f"  ✅ {template_file}: Has proper student-only condition")
                        else:
                            print(f"  ❌ {template_file}: Missing student-only condition")
                    elif 'Subscription Expired' in content or 'subscription expired' in content:
                        # Check for subscription status displays
                        if "user.user_type == 'student'" in content or 'student_dashboard' in template_file:
                            print(f"  ✅ {template_file}: Subscription status properly scoped")
                        else:
                            print(f"  ⚠️ {template_file}: Check subscription status scoping")
                            
                except Exception as e:
                    print(f"  ❌ Error reading {template_file}: {e}")
            else:
                print(f"  ⚠️ {template_file}: File not found")
    
    def run_tests(self):
        """Run all subscription alert tests"""
        print("=" * 70)
        print("SUBSCRIPTION ALERT VISIBILITY TEST")
        print("=" * 70)
        
        self.check_template_conditions()
        self.test_subscription_alert_visibility()
        
        print("\n" + "=" * 70)
        print("Tests completed")

if __name__ == '__main__':
    tester = SubscriptionAlertTest()
    tester.run_tests()
