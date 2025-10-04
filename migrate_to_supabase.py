#!/usr/bin/env python
"""
Script to migrate Django LMS data to Supabase
"""
import os
import sys
import django
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings_vercel')

# Setup Django
django.setup()

def migrate_to_supabase():
    """
    Migrate data from SQLite to Supabase PostgreSQL
    """
    from django.core.management import execute_from_command_line
    
    print("🚀 Starting migration to Supabase...")
    
    try:
        # Step 1: Create migrations
        print("📝 Creating migrations...")
        execute_from_command_line(['manage.py', 'makemigrations'])
        
        # Step 2: Apply migrations
        print("🔄 Applying migrations to Supabase...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        # Step 3: Create superuser (interactive)
        print("👤 Creating superuser...")
        execute_from_command_line(['manage.py', 'createsuperuser'])
        
        # Step 4: Collect static files
        print("📦 Collecting static files...")
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        
        print("✅ Migration completed successfully!")
        print("🌐 Your Django app is now connected to Supabase!")
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        return False
    
    return True

def export_current_data():
    """
    Export current data from SQLite (if exists)
    """
    try:
        from django.core.management import execute_from_command_line
        
        print("📤 Exporting current data...")
        execute_from_command_line([
            'manage.py', 'dumpdata', 
            '--natural-foreign', 
            '--natural-primary',
            '-e', 'contenttypes',
            '-e', 'auth.Permission',
            '--output=backup_data.json'
        ])
        print("✅ Data exported to backup_data.json")
        
    except Exception as e:
        print(f"⚠️ Could not export data: {str(e)}")

if __name__ == '__main__':
    print("🎯 Django LMS Supabase Migration Tool")
    print("=" * 50)
    
    # Check if we're using Supabase settings
    if 'settings_vercel' not in os.environ.get('DJANGO_SETTINGS_MODULE', ''):
        print("⚠️ Warning: Make sure DJANGO_SETTINGS_MODULE is set to 'library_system.settings_vercel'")
        print("Set it with: export DJANGO_SETTINGS_MODULE=library_system.settings_vercel")
    
    # Export current data first
    export_current_data()
    
    # Migrate to Supabase
    success = migrate_to_supabase()
    
    if success:
        print("\n🎉 Next steps:")
        print("1. Test your app locally with: python manage.py runserver")
        print("2. Deploy to Vercel with: vercel")
        print("3. Set environment variables in Vercel dashboard")
        print("4. Visit your deployed app!")
    else:
        print("\n❌ Please check the errors above and try again.")
