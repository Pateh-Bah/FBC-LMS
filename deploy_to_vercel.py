#!/usr/bin/env python
"""
Script to help deploy Django LMS to Vercel
"""
import os
import subprocess
import sys

def run_command(command, description):
    """
    Run a command and handle errors
    """
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Error: {e.stderr}")
        return False

def check_requirements():
    """
    Check if required tools are installed
    """
    print("🔍 Checking requirements...")
    
    # Check if Vercel CLI is installed
    try:
        subprocess.run(['vercel', '--version'], check=True, capture_output=True)
        print("✅ Vercel CLI is installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Vercel CLI is not installed")
        print("Install it with: npm install -g vercel")
        return False
    
    # Check if we're in a git repository
    try:
        subprocess.run(['git', 'status'], check=True, capture_output=True)
        print("✅ Git repository detected")
    except subprocess.CalledProcessError:
        print("❌ Not in a git repository")
        return False
    
    return True

def deploy_to_vercel():
    """
    Deploy to Vercel
    """
    print("🚀 Starting Vercel deployment...")
    
    # Step 1: Check requirements
    if not check_requirements():
        return False
    
    # Step 2: Login to Vercel (if not already logged in)
    print("🔐 Checking Vercel authentication...")
    try:
        subprocess.run(['vercel', 'whoami'], check=True, capture_output=True)
        print("✅ Already logged in to Vercel")
    except subprocess.CalledProcessError:
        print("🔑 Please login to Vercel:")
        if not run_command('vercel login', 'Login to Vercel'):
            return False
    
    # Step 3: Deploy
    print("🚀 Deploying to Vercel...")
    if not run_command('vercel --prod', 'Deploy to Vercel'):
        return False
    
    print("✅ Deployment completed!")
    return True

def show_next_steps():
    """
    Show next steps after deployment
    """
    print("\n🎯 Next Steps:")
    print("=" * 50)
    print("1. 🌐 Go to your Vercel dashboard")
    print("2. ⚙️ Set environment variables in Settings > Environment Variables:")
    print("   - SECRET_KEY")
    print("   - DATABASE_URL")
    print("   - SUPABASE_URL")
    print("   - SUPABASE_ANON_KEY")
    print("   - DJANGO_SETTINGS_MODULE=library_system.settings_vercel")
    print("3. 🔄 Redeploy after setting environment variables")
    print("4. 🧪 Test your deployed application")
    print("5. 📊 Monitor logs in Vercel dashboard")

if __name__ == '__main__':
    print("🎯 Django LMS Vercel Deployment Tool")
    print("=" * 50)
    
    # Check if we have the required files
    required_files = ['vercel.json', 'api/index.py', 'library_system/settings_vercel.py']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        print("Please make sure all configuration files are created first.")
        sys.exit(1)
    
    # Deploy to Vercel
    success = deploy_to_vercel()
    
    if success:
        show_next_steps()
    else:
        print("\n❌ Deployment failed. Please check the errors above.")
        sys.exit(1)
