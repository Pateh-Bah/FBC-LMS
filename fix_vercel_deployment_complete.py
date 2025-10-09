#!/usr/bin/env python
"""
Complete Vercel Deployment Fix Script
This script will fix all Vercel deployment issues and ensure proper deployment
"""
import os
import sys
import subprocess
import json
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

def check_vercel_login():
    """Check if user is logged into Vercel"""
    print("🔍 Checking Vercel login status...")
    
    try:
        result = subprocess.run(['vercel', 'whoami'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Logged in as: {result.stdout.strip()}")
            return True
        else:
            print("❌ Not logged into Vercel")
            return False
    except Exception as e:
        print(f"❌ Error checking Vercel login: {str(e)}")
        return False

def login_to_vercel():
    """Login to Vercel"""
    print("🔑 Logging into Vercel...")
    print("This will open a browser window for authentication.")
    
    try:
        subprocess.run(['vercel', 'login'], check=True)
        print("✅ Successfully logged into Vercel!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to login to Vercel: {str(e)}")
        return False

def check_required_files():
    """Check if all required files are present"""
    print("🔍 Checking required files...")
    
    required_files = [
        'vercel.json',
        'api/index.py',
        'library_system/settings_vercel.py',
        'requirements-vercel.txt'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files are present!")
    return True

def check_vercel_config():
    """Validate Vercel configuration"""
    print("🔍 Validating Vercel configuration...")
    
    try:
        with open('vercel.json', 'r') as f:
            config = json.load(f)
        
        # Check required fields
        required_fields = ['version', 'builds', 'routes', 'env']
        for field in required_fields:
            if field not in config:
                print(f"❌ Missing field in vercel.json: {field}")
                return False
        
        # Check Django settings module
        if config['env'].get('DJANGO_SETTINGS_MODULE') != 'library_system.settings_vercel':
            print("❌ Wrong Django settings module in vercel.json")
            return False
        
        print("✅ Vercel configuration is valid!")
        return True
        
    except Exception as e:
        print(f"❌ Error validating vercel.json: {str(e)}")
        return False

def collect_static_files():
    """Collect static files"""
    print("📦 Collecting static files...")
    
    # Set Django settings
    os.environ['DJANGO_SETTINGS_MODULE'] = 'library_system.settings_vercel'
    
    return run_command(
        'python manage.py collectstatic --noinput',
        'Collecting static files'
    )

def check_environment_setup():
    """Check if environment is properly set up"""
    print("🔍 Checking environment setup...")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("Please run: python setup_environment.py")
        return False
    
    # Check if environment variables are configured
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = ['SECRET_KEY', 'DATABASE_URL', 'SUPABASE_URL', 'SUPABASE_ANON_KEY']
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value or '<' in value or '>' in value:
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing or incomplete environment variables: {', '.join(missing_vars)}")
        print("Please update your .env file with actual Supabase credentials")
        return False
    
    print("✅ Environment setup looks good!")
    return True

def deploy_to_vercel():
    """Deploy to Vercel"""
    print("🚀 Deploying to Vercel...")
    
    # Deploy to production
    if run_command('vercel --prod', 'Deploy to Vercel production'):
        print("✅ Deployment successful!")
        return True
    else:
        print("❌ Deployment failed!")
        return False

def get_deployment_url():
    """Get deployment URL"""
    print("🌐 Getting deployment URL...")
    
    try:
        result = subprocess.run(['vercel', 'ls'], capture_output=True, text=True)
        if result.returncode == 0:
            print("📋 Your deployments:")
            print(result.stdout)
            
            # Try to get the production URL
            result = subprocess.run(['vercel', 'inspect', '--prod'], capture_output=True, text=True)
            if result.returncode == 0:
                print("📊 Production deployment details:")
                print(result.stdout)
        else:
            print("❌ Could not get deployment list")
    except Exception as e:
        print(f"❌ Error getting deployment URL: {str(e)}")

def show_environment_variables():
    """Show environment variables that need to be set in Vercel"""
    print("\n📋 Environment Variables for Vercel Dashboard:")
    print("=" * 60)
    
    from dotenv import load_dotenv
    load_dotenv()
    
    env_vars = [
        ("SECRET_KEY", os.getenv('SECRET_KEY', 'your-secret-key-here')),
        ("DEBUG", "False"),
        ("DJANGO_SETTINGS_MODULE", "library_system.settings_vercel"),
        ("DATABASE_URL", os.getenv('DATABASE_URL', 'your-database-url-here')),
        ("SUPABASE_URL", os.getenv('SUPABASE_URL', 'your-supabase-url-here')),
        ("SUPABASE_ANON_KEY", os.getenv('SUPABASE_ANON_KEY', 'your-anon-key-here')),
        ("SUPABASE_SERVICE_ROLE_KEY", os.getenv('SUPABASE_SERVICE_ROLE_KEY', 'your-service-role-key-here')),
        ("ANNUAL_SUBSCRIPTION_FEE", "100000"),
        ("FINE_PER_DAY", "5000"),
        ("ALLOWED_HOSTS", "localhost,127.0.0.1,*.vercel.app,*.vercel.app."),
    ]
    
    for key, value in env_vars:
        print(f"{key}={value}")
    
    print("\n⚠️ IMPORTANT:")
    print("1. Add these variables in Vercel Dashboard > Settings > Environment Variables")
    print("2. Redeploy after adding variables: vercel --prod")

def main():
    """Main fix function"""
    print("🎯 Complete Vercel Deployment Fix")
    print("=" * 50)
    
    # Step 1: Check Vercel login
    if not check_vercel_login():
        print("\n🔑 Step 1: Logging into Vercel...")
        if not login_to_vercel():
            print("❌ Please login to Vercel first!")
            print("Run: vercel login")
            return False
    
    # Step 2: Check required files
    print("\n🔍 Step 2: Checking required files...")
    if not check_required_files():
        print("❌ Missing required files!")
        return False
    
    # Step 3: Validate Vercel config
    print("\n🔍 Step 3: Validating Vercel configuration...")
    if not check_vercel_config():
        print("❌ Vercel configuration is invalid!")
        return False
    
    # Step 4: Check environment setup
    print("\n🔍 Step 4: Checking environment setup...")
    if not check_environment_setup():
        print("❌ Environment setup incomplete!")
        print("Please configure your .env file with Supabase credentials")
        return False
    
    # Step 5: Collect static files
    print("\n📦 Step 5: Collecting static files...")
    if not collect_static_files():
        print("❌ Failed to collect static files!")
        return False
    
    # Step 6: Deploy to Vercel
    print("\n🚀 Step 6: Deploying to Vercel...")
    if not deploy_to_vercel():
        print("❌ Deployment failed!")
        print("\n📋 Troubleshooting steps:")
        print("1. Check Vercel dashboard for build logs")
        print("2. Make sure all environment variables are set")
        print("3. Check that your code is committed to git")
        return False
    
    # Step 7: Get deployment info
    print("\n🌐 Step 7: Getting deployment information...")
    get_deployment_url()
    
    # Step 8: Show environment variables
    show_environment_variables()
    
    print("\n🎉 Deployment fix completed!")
    print("\n📋 Final Steps:")
    print("1. Go to your Vercel dashboard")
    print("2. Set environment variables in Settings > Environment Variables")
    print("3. Redeploy: vercel --prod")
    print("4. Your site should now be live!")
    
    return True

if __name__ == '__main__':
    success = main()
    if not success:
        print("\n❌ Fix failed. Please check the errors above.")
        sys.exit(1)
