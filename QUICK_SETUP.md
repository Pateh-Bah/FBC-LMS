# Quick Setup Guide - Django LMS to Vercel + Supabase

## Your Supabase Details
- **Project URL**: https://your-project.supabase.co
- **API Key**: <your-anon-key>

## Step 1: Get Database Connection String

1. Go to [Supabase Dashboard](https://supabase.com/dashboard)
2. Select your project
3. Go to **Settings** → **Database**
4. Copy the **Connection string** (URI format)
5. It should look like: `postgresql://postgres:<REDACTED_PASSWORD>@db.<your-project-id>.supabase.co:5432/postgres`

## Step 2: Set Environment Variables

Create a `.env` file in your project root:

```bash
# Django Settings
SECRET_KEY=your-secure-secret-key-here
DEBUG=False
DJANGO_SETTINGS_MODULE=library_system.settings_vercel

# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key

# Database Configuration (Replace [YOUR-PASSWORD] with your actual password)
DATABASE_URL=postgresql://postgres:<REDACTED_PASSWORD>@db.<your-project-id>.supabase.co:5432/postgres

# Email Configuration (Optional)
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
ALLOWED_HOSTS=localhost,127.0.0.1,*.vercel.app,*.vercel.app.,vkpbbepkwqenegbkxxli.supabase.co
```

## Step 3: Test Locally with Supabase

```bash
# Set environment variables
export DATABASE_URL="postgresql://postgres:[YOUR-PASSWORD]@db.vkpbbepkwqenegbkxxli.supabase.co:5432/postgres"
export DJANGO_SETTINGS_MODULE="library_system.settings_vercel"

# Run migrations
python migrate_to_supabase.py

# Test locally
python manage.py runserver
```

## Step 4: Deploy to Vercel

### Option A: Using the deployment script
```bash
python deploy_to_vercel.py
```

### Option B: Manual deployment
```bash
# Install Vercel CLI (if not installed)
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

## Step 5: Set Environment Variables in Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your project
3. Go to **Settings** → **Environment Variables**
4. Add all the environment variables from your `.env` file

## Step 6: Test Your Deployment

1. Visit your Vercel URL
2. Test the main functionality
3. Check if database operations work
4. Verify static files are loading

## Troubleshooting

### Common Issues:

1. **Database connection errors**:
   - Check your DATABASE_URL format
   - Ensure your Supabase project is active
   - Verify the password is correct

2. **Static files not loading**:
   - Check WhiteNoise configuration
   - Ensure static files are collected

3. **Cold starts**:
   - Normal with serverless functions
   - Consider Railway or Render for better performance

### Debug Mode:
Set `DEBUG=True` temporarily to see detailed error messages.

## Alternative Deployment (Recommended)

Since Vercel has limitations with Django, consider:

### Railway (Recommended)
1. Go to [railway.app](https://railway.app)
2. Connect your GitHub repository
3. Add environment variables
4. Deploy automatically

### Render
1. Go to [render.com](https://render.com)
2. Create new Web Service
3. Connect GitHub repository
4. Configure build and start commands

## Support

If you encounter issues:
1. Check Vercel function logs
2. Check Supabase logs
3. Test locally with production settings
4. Review the full DEPLOYMENT_GUIDE.md
