#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
django.setup()

from django.test import RequestFactory
from fbc_users.context_processors import system_settings_context

def test_context_processor():
    print("Testing system settings context processor...")
    
    # Create a fake request
    factory = RequestFactory()
    request = factory.get('/test/')
    
    # Get context from processor
    context = system_settings_context(request)
    
    print("\nContext processor output:")
    for key, value in context.items():
        print(f"  {key}: {value}")
    
    # Check specifically for logo
    if context.get('system_logo'):
        print(f"\n✅ Logo URL found: {context['system_logo']}")
    else:
        print("\n❌ No logo URL in context")
    
    print(f"\n✅ System name: {context.get('system_name', 'Not found')}")

if __name__ == "__main__":
    test_context_processor()
