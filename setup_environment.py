#!/usr/bin/env python
"""
Environment setup script for Django LMS
This script will help you create the necessary environment files for deployment
"""
import os
import secrets
import string

def generate_secret_key():
    """Generate a secure Django secret key"""
    return ''.join(secrets.choice(string.ascii_letters + string.digits + '!@#$%^&*(-_=+)') for _ in range(50))

def create_env_file():
    """Create .env file with template values"""
    env_content = f"""# Django Settings
SECRET_KEY={generate_secret_key()}
DEBUG=False
DJANGO_SETTINGS_MODULE=library_system.settings_vercel

# Database Configuration (Supabase)
# Replace <YOUR-PASSWORD> with your actual Supabase database password
# Replace <your-project-id> with your actual Supabase project ID
DATABASE_URL=postgresql://postgres:<YOUR-PASSWORD>@db.<your-project-id>.supabase.co:5432/postgres?sslmode=require

# Supabase Configuration
SUPABASE_URL=https://<your-project-id>.supabase.co
SUPABASE_ANON_KEY=<your-supabase-anon-key>
SUPABASE_SERVICE_ROLE_KEY=<your-supabase-service-role-key>

# Email Configuration (Optional - can use Supabase SMTP)
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_PORT=587
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=noreply@fbc-lms.com

# Library Settings
ANNUAL_SUBSCRIPTION_FEE=100000
FINE_PER_DAY=5000

# Vercel Configuration
ALLOWED_HOSTS=localhost,127.0.0.1,*.vercel.app,*.vercel.app.
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env file with template values")
    print("⚠️  IMPORTANT: Please edit .env file and replace the placeholder values with your actual credentials!")

def main():
    """Main setup function"""
    print("🎯 Django LMS Environment Setup")
    print("=" * 50)
    
    if os.path.exists('.env'):
        print("⚠️  .env file already exists!")
        overwrite = input("Do you want to overwrite it? (y/n): ").lower().strip()
        if overwrite != 'y':
            print("❌ Setup cancelled")
            return
    
    create_env_file()
    
    print("\n📋 Next Steps:")
    print("1. Edit .env file with your actual Supabase credentials")
    print("2. Get your Supabase database password from your Supabase dashboard")
    print("3. Replace <your-project-id> with your actual Supabase project ID")
    print("4. Replace <YOUR-PASSWORD> with your actual database password")
    print("5. Get your Supabase API keys from Settings > API in your Supabase dashboard")
    print("\n🔗 Supabase Dashboard: https://supabase.com/dashboard")
    print("📖 Documentation: Check DEPLOYMENT_GUIDE.md for detailed instructions")

if __name__ == '__main__':
    main()
