#!/usr/bin/env python
"""
Setup script for Django LMS deployment to Vercel
This script helps you set up the environment and deploy to Vercel
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description, check=True):
    """
    Run a command and handle errors
    """
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

def check_virtual_environment():
    """
    Check if we're in a virtual environment
    """
    print("🔍 Checking virtual environment...")
    
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment detected!")
        print(f"Python executable: {sys.executable}")
        return True
    else:
        print("⚠️ No virtual environment detected!")
        print("Please activate your virtual environment first:")
        print("On Windows: venv\\Scripts\\activate")
        print("On Mac/Linux: source venv/bin/activate")
        return False

def install_requirements():
    """
    Install requirements from requirements.txt
    """
    print("📦 Installing requirements...")
    
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt not found!")
        return False
    
    return run_command('pip install -r requirements.txt', 'Installing Python packages')

def create_env_file():
    """
    Create .env file from template if it doesn't exist
    """
    print("📝 Setting up environment file...")
    
    env_file = '.env'
    if os.path.exists(env_file):
        print(f"✅ {env_file} already exists")
        return True
    
    # Copy from template (use env.example only; do not store real secrets in the repo)
    template_files = ['env.example']
    for template in template_files:
        if os.path.exists(template):
            shutil.copy(template, env_file)
            print(f"✅ Created {env_file} from {template}")
            print(f"⚠️ Please edit {env_file} and add your Supabase database password!")
            return True
    
    print("❌ No environment template found!")
    return False

def check_vercel_cli():
    """
    Check if Vercel CLI is installed
    """
    print("🔍 Checking Vercel CLI...")
    
    try:
        subprocess.run(['vercel', '--version'], check=True, capture_output=True)
        print("✅ Vercel CLI is installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Vercel CLI is not installed")
        print("Installing Vercel CLI...")
        return run_command('npm install -g vercel', 'Installing Vercel CLI')

def setup_database():
    """
    Setup database connection and run migrations
    """
    print("🗄️ Setting up database...")
    
    # Check if DATABASE_URL is set
    if not os.getenv('DATABASE_URL'):
        print("⚠️ DATABASE_URL not found in environment variables")
        print("Please set it in your .env file with your Supabase database password")
        return False
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings_vercel')
    
    # Run migrations
    if run_command('python manage.py makemigrations', 'Creating migrations', check=False):
        run_command('python manage.py migrate', 'Running migrations')
    
    # Collect static files
    run_command('python manage.py collectstatic --noinput', 'Collecting static files')
    
    return True

def deploy_to_vercel():
    """
    Deploy to Vercel
    """
    print("🚀 Deploying to Vercel...")
    
    # Check if user is logged in
    try:
        subprocess.run(['vercel', 'whoami'], check=True, capture_output=True)
        print("✅ Already logged in to Vercel")
    except subprocess.CalledProcessError:
        print("🔑 Please login to Vercel:")
        if not run_command('vercel login', 'Login to Vercel'):
            return False
    
    # Deploy
    return run_command('vercel --prod', 'Deploying to Vercel')

def show_environment_variables():
    """
    Show environment variables that need to be set in Vercel
    """
    print("\n📋 Environment Variables for Vercel Dashboard:")
    print("=" * 60)
    
    env_vars = [
        ("SECRET_KEY", "<REDACTED - SET IN VERCEL/GITHUB SECRETS>"),
        ("DEBUG", "False"),
        ("DJANGO_SETTINGS_MODULE", "library_system.settings_vercel"),
        ("SUPABASE_URL", "https://<your-project-id>.supabase.co"),
        ("SUPABASE_ANON_KEY", "<REDACTED_SUPABASE_ANON_KEY>"),
        ("SUPABASE_SERVICE_ROLE_KEY", "<REDACTED_SUPABASE_SERVICE_ROLE_KEY>"),
        ("DATABASE_URL", "postgresql://postgres:<REDACTED_PASSWORD>@db.<your-project-id>.supabase.co:5432/postgres"),
        ("ANNUAL_SUBSCRIPTION_FEE", "100000"),
        ("FINE_PER_DAY", "5000"),
        ("ALLOWED_HOSTS", "localhost,127.0.0.1,*.vercel.app"),
    ]
    
    for key, value in env_vars:
        print(f"{key}={value}")
    
    print("\n⚠️ IMPORTANT:")
    print("1. Replace [YOUR-PASSWORD] with your actual Supabase database password")
    print("2. Change SECRET_KEY to a secure random string")
    print("3. Add these variables in Vercel Dashboard > Settings > Environment Variables")

def main():
    """
    Main setup function
    """
    print("🎯 Django LMS Vercel Setup Tool")
    print("=" * 50)
    
    # Step 1: Check virtual environment
    if not check_virtual_environment():
        print("\n❌ Please activate your virtual environment and run this script again.")
        return False
    
    # Step 2: Install requirements
    if not install_requirements():
        print("\n❌ Failed to install requirements. Please check requirements.txt")
        return False
    
    # Step 3: Create environment file
    create_env_file()
    
    # Step 4: Check Vercel CLI
    if not check_vercel_cli():
        print("\n❌ Failed to install Vercel CLI")
        return False
    
    # Step 5: Show environment variables
    show_environment_variables()
    
    # Step 6: Ask about database setup
    print("\n🗄️ Database Setup:")
    print("Before deploying, you need to:")
    print("1. Get your Supabase database password")
    print("2. Update the DATABASE_URL in your .env file")
    print("3. Run: python manage.py migrate")
    print("4. Create a superuser: python manage.py createsuperuser")
    
    # Step 7: Ask about deployment
    deploy_choice = input("\n🚀 Do you want to deploy to Vercel now? (y/n): ").lower().strip()
    
    if deploy_choice == 'y':
        if deploy_to_vercel():
            print("\n✅ Deployment completed!")
            print("📋 Don't forget to set environment variables in Vercel dashboard!")
        else:
            print("\n❌ Deployment failed. Please check the errors above.")
    else:
        print("\n📝 To deploy later, run: vercel --prod")
    
    print("\n🎉 Setup completed!")
    print("📖 Check QUICK_SETUP.md for detailed instructions")

if __name__ == '__main__':
    main()
