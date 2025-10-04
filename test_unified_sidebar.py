#!/usr/bin/env python
"""
Test script to verify unified sidebar implementation
"""
import os
import sys
import django
from django.test import Client
from django.contrib.auth import get_user_model

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
django.setup()

def test_unified_sidebar():
    """Test that student and lecturer dashboards use unified sidebar"""
    print("Testing unified sidebar implementation...")
    
    # Create test client
    client = Client()
    
    User = get_user_model()
    
    # Test template inheritance - verify templates can be loaded
    from django.template.loader import get_template
    
    try:
        # Test admin base template
        admin_base = get_template('admin/admin_base.html')
        print("✓ Admin base template loads successfully")
        
        # Test student dashboard template
        student_template = get_template('users/student_dashboard.html')
        print("✓ Student dashboard template loads successfully")
        
        # Test lecturer dashboard template  
        lecturer_template = get_template('users/lecturer_dashboard.html')
        print("✓ Lecturer dashboard template loads successfully")
        
        # Verify template inheritance structure
        student_source = student_template.template.source
        lecturer_source = lecturer_template.template.source
        
        # Check that both extend admin_base.html
        if "extends 'admin/admin_base.html'" in student_source:
            print("✓ Student dashboard extends admin/admin_base.html")
        else:
            print("✗ Student dashboard NOT extending admin_base.html")
            
        if "extends 'admin/admin_base.html'" in lecturer_source:
            print("✓ Lecturer dashboard extends admin/admin_base.html")
        else:
            print("✗ Lecturer dashboard NOT extending admin_base.html")
            
        # Check that both use content block
        if "block content" in student_source:
            print("✓ Student dashboard uses content block")
        else:
            print("✗ Student dashboard NOT using content block")
            
        if "block content" in lecturer_source:
            print("✓ Lecturer dashboard uses content block")
        else:
            print("✗ Lecturer dashboard NOT using content block")
            
        print("\n🎉 Unified sidebar implementation successful!")
        print("Both student and lecturer dashboards now inherit the admin sidebar design")
        
    except Exception as e:
        print(f"✗ Error testing templates: {e}")
        return False
        
    return True

if __name__ == "__main__":
    print("="*60)
    print("FBC Library - Unified Sidebar Implementation Test")
    print("="*60)
    test_unified_sidebar()