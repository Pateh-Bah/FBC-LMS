#!/usr/bin/env python
"""
Quick Fix Script for Django LMS Connection Issues
This script will help you quickly fix the most common connection problems
"""
import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description, check=True):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.stdout:
            print(f"✅ {description} completed!")
            if result.stdout.strip():
                print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def check_environment():
    """Check current environment setup"""
    print("🔍 Checking environment setup...")
    
    # Check if .env exists
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("Run: python setup_environment.py")
        return False
    
    # Check environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = [
        'SECRET_KEY',
        'DATABASE_URL',
        'SUPABASE_URL',
        'DJANGO_SETTINGS_MODULE'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    print("✅ Environment setup looks good!")
    return True

def test_django_config():
    """Test Django configuration"""
    print("🔍 Testing Django configuration...")
    
    # Set environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings_vercel')
    
    # Test Django check
    if run_command('python manage.py check --settings=library_system.settings_vercel', 'Django system check', check=False):
        print("✅ Django configuration is valid!")
        return True
    else:
        print("❌ Django configuration has issues!")
        return False

def test_database_connection():
    """Test database connection"""
    print("🔍 Testing database connection...")
    
    try:
        # Import Django and test database
        import django
        from django.conf import settings
        from django.db import connection
        
        django.setup()
        
        # Test connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            
        if result:
            print("✅ Database connection successful!")
            return True
        else:
            print("❌ Database connection failed!")
            return False
            
    except Exception as e:
        print(f"❌ Database connection error: {str(e)}")
        return False

def collect_static_files():
    """Collect static files"""
    print("📦 Collecting static files...")
    return run_command(
        'python manage.py collectstatic --noinput --settings=library_system.settings_vercel',
        'Collecting static files'
    )

def run_migrations():
    """Run database migrations"""
    print("🔄 Running database migrations...")
    
    # Make migrations first
    if run_command('python manage.py makemigrations --settings=library_system.settings_vercel', 'Creating migrations', check=False):
        # Then apply migrations
        return run_command('python manage.py migrate --settings=library_system.settings_vercel', 'Applying migrations')
    else:
        print("⚠️ No new migrations to create")
        return run_command('python manage.py migrate --settings=library_system.settings_vercel', 'Applying migrations')

def main():
    """Main fix function"""
    print("🎯 Django LMS Connection Fix Tool")
    print("=" * 50)
    
    # Step 1: Check environment
    if not check_environment():
        print("\n❌ Please fix environment setup first!")
        print("Run: python setup_environment.py")
        return False
    
    # Step 2: Test Django config
    if not test_django_config():
        print("\n❌ Please fix Django configuration!")
        return False
    
    # Step 3: Test database connection
    if not test_database_connection():
        print("\n❌ Please check your DATABASE_URL in .env file!")
        print("Make sure your Supabase credentials are correct.")
        return False
    
    # Step 4: Run migrations
    if not run_migrations():
        print("\n❌ Migration failed!")
        return False
    
    # Step 5: Collect static files
    if not collect_static_files():
        print("\n❌ Static files collection failed!")
        return False
    
    print("\n🎉 All checks passed!")
    print("\n📋 Next Steps:")
    print("1. Test locally: python manage.py runserver")
    print("2. Deploy to Vercel: vercel --prod")
    print("3. Set environment variables in Vercel dashboard")
    print("4. Redeploy: vercel --prod")
    
    return True

if __name__ == '__main__':
    success = main()
    if not success:
        sys.exit(1)
