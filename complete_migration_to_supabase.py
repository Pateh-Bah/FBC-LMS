#!/usr/bin/env python
"""
Complete Migration Script: SQLite to Supabase
This script will migrate all your SQLite data to Supabase PostgreSQL
"""
import os
import sys
import json
import django
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

def setup_django_for_migration():
    """Setup Django with local SQLite settings for data export"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')
    django.setup()
    return True

def export_sqlite_data():
    """Export all data from SQLite database"""
    print("📤 Exporting data from SQLite database...")
    
    try:
        from django.core.management import execute_from_command_line
        
        # Export all data except Django system tables
        execute_from_command_line([
            'manage.py', 'dumpdata',
            '--natural-foreign',
            '--natural-primary',
            '-e', 'contenttypes',
            '-e', 'auth.Permission',
            '-e', 'sessions',
            '--output=sqlite_backup.json',
            '--indent=2'
        ])
        
        print("✅ SQLite data exported to sqlite_backup.json")
        
        # Check the backup file
        if os.path.exists('sqlite_backup.json'):
            with open('sqlite_backup.json', 'r') as f:
                data = json.load(f)
            print(f"📊 Exported {len(data)} records from SQLite")
            return True
        else:
            print("❌ Backup file not created!")
            return False
            
    except Exception as e:
        print(f"❌ Error exporting SQLite data: {str(e)}")
        return False

def setup_supabase_connection():
    """Setup connection to Supabase"""
    print("🔗 Setting up Supabase connection...")
    
    # Check if .env file exists and has Supabase credentials
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("Please run: python setup_environment.py")
        return False
    
    from dotenv import load_dotenv
    load_dotenv()
    
    # Check required environment variables
    required_vars = [
        'DATABASE_URL',
        'SUPABASE_URL',
        'SUPABASE_ANON_KEY'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value or '<' in value or '>' in value:
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing or incomplete environment variables: {', '.join(missing_vars)}")
        print("Please update your .env file with actual Supabase credentials")
        return False
    
    print("✅ Supabase credentials found in .env file")
    return True

def migrate_to_supabase():
    """Migrate to Supabase PostgreSQL"""
    print("🚀 Starting migration to Supabase...")
    
    try:
        from django.core.management import execute_from_command_line
        
        # Switch to Supabase settings
        os.environ['DJANGO_SETTINGS_MODULE'] = 'library_system.settings_vercel'
        
        # Re-setup Django with Supabase settings
        django.setup()
        
        # Step 1: Create migrations
        print("📝 Creating migrations for Supabase...")
        execute_from_command_line(['manage.py', 'makemigrations'])
        
        # Step 2: Apply migrations
        print("🔄 Applying migrations to Supabase...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        print("✅ Database schema created in Supabase")
        return True
        
    except Exception as e:
        print(f"❌ Error creating Supabase schema: {str(e)}")
        return False

def import_data_to_supabase():
    """Import exported data to Supabase"""
    print("📥 Importing data to Supabase...")
    
    try:
        from django.core.management import execute_from_command_line
        
        # Import the backed up data
        execute_from_command_line([
            'manage.py', 'loaddata',
            'sqlite_backup.json'
        ])
        
        print("✅ Data successfully imported to Supabase!")
        return True
        
    except Exception as e:
        print(f"❌ Error importing data to Supabase: {str(e)}")
        return False

def verify_migration():
    """Verify that data was migrated correctly"""
    print("🔍 Verifying migration...")
    
    try:
        from django.contrib.auth import get_user_model
        from fbc_books.models import Book, Author, Category
        from fbc_payments.models import Payment
        
        User = get_user_model()
        
        # Count records
        user_count = User.objects.count()
        book_count = Book.objects.count()
        author_count = Author.objects.count()
        category_count = Category.objects.count()
        payment_count = Payment.objects.count()
        
        print(f"📊 Supabase Data Verification:")
        print(f"   Users: {user_count}")
        print(f"   Books: {book_count}")
        print(f"   Authors: {author_count}")
        print(f"   Categories: {category_count}")
        print(f"   Payments: {payment_count}")
        
        # Test a sample query
        if user_count > 0:
            sample_user = User.objects.first()
            print(f"   Sample user: {sample_user.username} ({sample_user.email})")
        
        if book_count > 0:
            sample_book = Book.objects.first()
            print(f"   Sample book: {sample_book.title}")
        
        print("✅ Migration verification completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error verifying migration: {str(e)}")
        return False

def create_superuser():
    """Create superuser in Supabase"""
    print("👤 Creating superuser in Supabase...")
    
    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'createsuperuser'])
        print("✅ Superuser created successfully!")
        return True
        
    except Exception as e:
        print(f"⚠️ Could not create superuser: {str(e)}")
        print("You can create one later with: python manage.py createsuperuser --settings=library_system.settings_vercel")
        return False

def collect_static_files():
    """Collect static files for deployment"""
    print("📦 Collecting static files...")
    
    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        print("✅ Static files collected!")
        return True
        
    except Exception as e:
        print(f"❌ Error collecting static files: {str(e)}")
        return False

def main():
    """Main migration function"""
    print("🎯 Complete Migration: SQLite to Supabase")
    print("=" * 60)
    
    # Step 1: Setup Django for SQLite export
    print("🔧 Step 1: Setting up Django for data export...")
    if not setup_django_for_migration():
        print("❌ Failed to setup Django")
        return False
    
    # Step 2: Export SQLite data
    print("\n📤 Step 2: Exporting SQLite data...")
    if not export_sqlite_data():
        print("❌ Failed to export SQLite data")
        return False
    
    # Step 3: Setup Supabase connection
    print("\n🔗 Step 3: Setting up Supabase connection...")
    if not setup_supabase_connection():
        print("❌ Failed to setup Supabase connection")
        print("\n📋 Please follow these steps:")
        print("1. Go to https://supabase.com/dashboard")
        print("2. Create a new project or use existing one")
        print("3. Get your database password from Settings > Database")
        print("4. Get your API keys from Settings > API")
        print("5. Update your .env file with these credentials")
        print("6. Run this script again")
        return False
    
    # Step 4: Migrate to Supabase
    print("\n🚀 Step 4: Creating Supabase database schema...")
    if not migrate_to_supabase():
        print("❌ Failed to create Supabase schema")
        return False
    
    # Step 5: Import data
    print("\n📥 Step 5: Importing data to Supabase...")
    if not import_data_to_supabase():
        print("❌ Failed to import data to Supabase")
        return False
    
    # Step 6: Verify migration
    print("\n🔍 Step 6: Verifying migration...")
    if not verify_migration():
        print("❌ Migration verification failed")
        return False
    
    # Step 7: Create superuser
    print("\n👤 Step 7: Creating superuser...")
    create_superuser()
    
    # Step 8: Collect static files
    print("\n📦 Step 8: Collecting static files...")
    collect_static_files()
    
    print("\n🎉 Migration completed successfully!")
    print("\n📋 Next Steps:")
    print("1. Test locally: python manage.py runserver --settings=library_system.settings_vercel")
    print("2. Deploy to Vercel: vercel --prod")
    print("3. Set environment variables in Vercel dashboard")
    print("4. Your data is now synced with Supabase!")
    
    return True

if __name__ == '__main__':
    success = main()
    if not success:
        print("\n❌ Migration failed. Please check the errors above.")
        sys.exit(1)
