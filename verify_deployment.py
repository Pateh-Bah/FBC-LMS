#!/usr/bin/env python
"""
Deployment Verification Script
This script will verify that your deployment is working correctly
"""
import os
import sys
import django
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

def setup_django():
    """Setup Django with Supabase settings"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings_vercel')
    django.setup()

def check_environment_variables():
    """Check if all required environment variables are set"""
    print("🔍 Checking environment variables...")
    
    required_vars = [
        'SECRET_KEY',
        'DATABASE_URL',
        'SUPABASE_URL',
        'SUPABASE_ANON_KEY',
        'DJANGO_SETTINGS_MODULE'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
        elif '<' in value or '>' in value:
            missing_vars.append(f"{var} (contains placeholder)")
    
    if missing_vars:
        print(f"❌ Missing or incomplete environment variables: {', '.join(missing_vars)}")
        return False
    
    print("✅ All environment variables are properly configured!")
    return True

def test_database_connection():
    """Test Supabase database connection"""
    print("🔍 Testing database connection...")
    
    try:
        from django.db import connection
        from django.db.utils import OperationalError
        
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
            
    except OperationalError as e:
        print(f"❌ Database connection error: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

def verify_data_migration():
    """Verify that data was migrated correctly"""
    print("🔍 Verifying data migration...")
    
    try:
        from django.contrib.auth import get_user_model
        from fbc_books.models import Book, Author, Category, BookBorrowing
        from fbc_payments.models import Payment
        from fbc_fines.models import Fine
        from fbc_users.models import SystemSettings
        
        User = get_user_model()
        
        # Count records
        user_count = User.objects.count()
        book_count = Book.objects.count()
        author_count = Author.objects.count()
        category_count = Category.objects.count()
        borrowing_count = BookBorrowing.objects.count()
        payment_count = Payment.objects.count()
        fine_count = Fine.objects.count()
        settings_count = SystemSettings.objects.count()
        
        print(f"📊 Data Verification Results:")
        print(f"   Users: {user_count}")
        print(f"   Books: {book_count}")
        print(f"   Authors: {author_count}")
        print(f"   Categories: {category_count}")
        print(f"   Borrowings: {borrowing_count}")
        print(f"   Payments: {payment_count}")
        print(f"   Fines: {fine_count}")
        print(f"   Settings: {settings_count}")
        
        # Expected counts based on your SQLite data
        expected_counts = {
            'users': 10,
            'books': 9,
            'authors': 10,
            'categories': 10,
            'borrowings': 18,
            'payments': 2,
            'fines': 1,
            'settings': 1
        }
        
        actual_counts = {
            'users': user_count,
            'books': book_count,
            'authors': author_count,
            'categories': category_count,
            'borrowings': borrowing_count,
            'payments': payment_count,
            'fines': fine_count,
            'settings': settings_count
        }
        
        # Check if counts match
        mismatches = []
        for table, expected in expected_counts.items():
            actual = actual_counts[table]
            if actual != expected:
                mismatches.append(f"{table}: expected {expected}, got {actual}")
        
        if mismatches:
            print(f"⚠️  Data count mismatches: {', '.join(mismatches)}")
            return False
        
        print("✅ All data counts match expected values!")
        
        # Test sample queries
        if user_count > 0:
            sample_user = User.objects.first()
            print(f"   Sample user: {sample_user.username} ({sample_user.email})")
        
        if book_count > 0:
            sample_book = Book.objects.first()
            print(f"   Sample book: {sample_book.title}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verifying data: {str(e)}")
        return False

def test_django_functionality():
    """Test basic Django functionality"""
    print("🔍 Testing Django functionality...")
    
    try:
        from django.core.management import execute_from_command_line
        
        # Run Django system check
        execute_from_command_line(['manage.py', 'check'])
        print("✅ Django system check passed!")
        
        # Test static files
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        print("✅ Static files collection successful!")
        
        return True
        
    except Exception as e:
        print(f"❌ Django functionality test failed: {str(e)}")
        return False

def test_vercel_configuration():
    """Test Vercel configuration"""
    print("🔍 Testing Vercel configuration...")
    
    # Check if vercel.json exists
    if not os.path.exists('vercel.json'):
        print("❌ vercel.json not found!")
        return False
    
    # Check if api/index.py exists
    if not os.path.exists('api/index.py'):
        print("❌ api/index.py not found!")
        return False
    
    # Check if staticfiles directory exists
    if not os.path.exists('staticfiles'):
        print("❌ staticfiles directory not found!")
        print("Run: python manage.py collectstatic --noinput")
        return False
    
    print("✅ Vercel configuration files are present!")
    return True

def main():
    """Main verification function"""
    print("🎯 Deployment Verification")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Test 1: Environment variables
    if not check_environment_variables():
        all_tests_passed = False
    
    # Test 2: Database connection
    if not test_database_connection():
        all_tests_passed = False
    
    # Test 3: Data migration
    if not verify_data_migration():
        all_tests_passed = False
    
    # Test 4: Django functionality
    if not test_django_functionality():
        all_tests_passed = False
    
    # Test 5: Vercel configuration
    if not test_vercel_configuration():
        all_tests_passed = False
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 All verification tests passed!")
        print("✅ Your deployment is ready!")
        print("\n📋 Final Steps:")
        print("1. Deploy to Vercel: vercel --prod")
        print("2. Set environment variables in Vercel dashboard")
        print("3. Redeploy: vercel --prod")
        print("4. Test your live application")
        return True
    else:
        print("❌ Some verification tests failed!")
        print("Please fix the issues above before deploying.")
        return False

if __name__ == '__main__':
    setup_django()
    success = main()
    if not success:
        sys.exit(1)
