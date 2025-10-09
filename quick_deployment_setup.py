#!/usr/bin/env python
"""
Quick Deployment Setup Script
This script will guide you through the complete deployment process
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

def check_prerequisites():
    """Check if all prerequisites are met"""
    print("🔍 Checking prerequisites...")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("Please run: python setup_environment.py")
        return False
    
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
    
    print("✅ All prerequisites met!")
    return True

def setup_supabase_credentials():
    """Guide user through Supabase setup"""
    print("\n🔗 Supabase Setup Guide")
    print("=" * 50)
    
    print("📋 Please follow these steps:")
    print("1. Go to https://supabase.com/dashboard")
    print("2. Create a new project (or use existing)")
    print("3. Get your database password from Settings > Database")
    print("4. Get your API keys from Settings > API")
    print("5. Update your .env file with these credentials")
    
    # Check if .env has placeholder values
    with open('.env', 'r') as f:
        env_content = f.read()
    
    if '<' in env_content and '>' in env_content:
        print("\n⚠️  Your .env file still contains placeholder values!")
        print("Please edit .env file and replace all <placeholder> values with your actual Supabase credentials.")
        
        continue_setup = input("\nHave you updated the .env file with your actual Supabase credentials? (y/n): ").lower().strip()
        if continue_setup != 'y':
            print("❌ Please update your .env file first and run this script again.")
            return False
    
    print("✅ Supabase credentials configured!")
    return True

def run_migration():
    """Run the complete migration"""
    print("\n🚀 Running data migration...")
    return run_command('python complete_migration_to_supabase.py', 'Complete migration to Supabase')

def test_local_deployment():
    """Test local deployment"""
    print("\n🧪 Testing local deployment...")
    
    # Test Django configuration
    if not run_command('python manage.py check --settings=library_system.settings_vercel', 'Django configuration check'):
        return False
    
    print("✅ Local deployment test passed!")
    print("You can test locally with: python manage.py runserver --settings=library_system.settings_vercel")
    
    return True

def deploy_to_vercel():
    """Deploy to Vercel"""
    print("\n🚀 Deploying to Vercel...")
    
    # Check if user is logged in
    try:
        subprocess.run(['vercel', 'whoami'], check=True, capture_output=True)
        print("✅ Already logged in to Vercel")
    except subprocess.CalledProcessError:
        print("🔑 Please login to Vercel:")
        if not run_command('vercel login', 'Login to Vercel'):
            return False
    
    # Deploy
    return run_command('vercel --prod', 'Deploy to Vercel')

def show_next_steps():
    """Show next steps after deployment"""
    print("\n🎯 Next Steps:")
    print("=" * 50)
    print("1. 🌐 Go to your Vercel dashboard")
    print("2. ⚙️ Set environment variables in Settings > Environment Variables:")
    print("   - Copy all variables from your .env file")
    print("   - Paste them into Vercel dashboard")
    print("3. 🔄 Redeploy after setting environment variables:")
    print("   vercel --prod")
    print("4. 🧪 Test your deployed application")
    print("5. 📊 Monitor logs in Vercel dashboard")
    print("\n📖 For detailed instructions, see COMPLETE_DEPLOYMENT_GUIDE.md")

def main():
    """Main deployment function"""
    print("🎯 Django FBC-LMS Quick Deployment Setup")
    print("=" * 60)
    
    # Step 1: Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites not met. Please fix the issues above.")
        return False
    
    # Step 2: Setup Supabase credentials
    if not setup_supabase_credentials():
        return False
    
    # Step 3: Run migration
    print("\n🔄 Step 3: Migrating data to Supabase...")
    if not run_migration():
        print("\n❌ Migration failed. Please check the errors above.")
        return False
    
    # Step 4: Test local deployment
    if not test_local_deployment():
        print("\n❌ Local deployment test failed.")
        return False
    
    # Step 5: Deploy to Vercel
    print("\n🚀 Step 5: Deploying to Vercel...")
    if not deploy_to_vercel():
        print("\n❌ Vercel deployment failed.")
        return False
    
    # Step 6: Show next steps
    show_next_steps()
    
    print("\n🎉 Deployment setup completed!")
    print("Your Django FBC-LMS is now ready for production!")
    
    return True

if __name__ == '__main__':
    success = main()
    if not success:
        print("\n❌ Deployment setup failed. Please check the errors above.")
        sys.exit(1)
