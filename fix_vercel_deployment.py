#!/usr/bin/env python
"""
Fix Vercel Deployment Issues
This script will help you resolve the "No Production Deployment" error
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
    
    required_vars = ['DATABASE_URL', 'SUPABASE_URL', 'SUPABASE_ANON_KEY']
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

def check_vercel_config():
    """Check Vercel configuration files"""
    print("🔍 Checking Vercel configuration...")
    
    required_files = ['vercel.json', 'api/index.py']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    print("✅ Vercel configuration files are present!")
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

def show_deployment_url():
    """Show deployment URL"""
    print("🌐 Getting deployment URL...")
    
    try:
        result = subprocess.run(['vercel', 'ls'], capture_output=True, text=True)
        if result.returncode == 0:
            print("📋 Your deployments:")
            print(result.stdout)
        else:
            print("❌ Could not get deployment list")
    except Exception as e:
        print(f"❌ Error getting deployment URL: {str(e)}")

def main():
    """Main fix function"""
    print("🎯 Fixing Vercel Deployment Issues")
    print("=" * 50)
    
    # Step 1: Check Vercel login
    if not check_vercel_login():
        print("\n🔑 Step 1: Logging into Vercel...")
        if not login_to_vercel():
            print("❌ Please login to Vercel first!")
            print("Run: vercel login")
            return False
    
    # Step 2: Check environment setup
    print("\n🔍 Step 2: Checking environment setup...")
    if not check_environment_setup():
        print("❌ Please configure your environment first!")
        print("1. Update .env file with your Supabase credentials")
        print("2. Run: python complete_migration_to_supabase.py")
        return False
    
    # Step 3: Check Vercel config
    print("\n🔍 Step 3: Checking Vercel configuration...")
    if not check_vercel_config():
        print("❌ Vercel configuration is incomplete!")
        return False
    
    # Step 4: Deploy to Vercel
    print("\n🚀 Step 4: Deploying to Vercel...")
    if not deploy_to_vercel():
        print("❌ Deployment failed!")
        print("\n📋 Troubleshooting steps:")
        print("1. Check Vercel dashboard for build logs")
        print("2. Make sure all environment variables are set")
        print("3. Check that your code is committed to git")
        return False
    
    # Step 5: Show deployment info
    print("\n🌐 Step 5: Deployment information...")
    show_deployment_url()
    
    print("\n🎉 Deployment fixed!")
    print("\n📋 Next Steps:")
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
