# Security Policy

## Environment Variables

This project uses environment variables for configuration. Never commit actual secrets or API keys to the repository.

1. Copy `env.example` to `.env`:
   ```bash
   cp env.example .env
   ```

2. Update `.env` with your actual values:
   - Generate a new Django SECRET_KEY
   - Add your Supabase credentials
   - Configure your email settings
   - Set your subscription fees

3. For production:
   - Use different secrets than development
   - Store secrets securely in your deployment platform
   - Regularly rotate sensitive credentials

## Reporting Security Issues

If you discover a security vulnerability, please send an email to [your-security-email]. All security vulnerabilities will be promptly addressed.

## Best Practices

1. Never commit `.env` files
2. Never share API keys in code or comments
3. Use environment variables for all secrets
4. Regularly rotate production credentials
5. Use strong, unique passwords and keys