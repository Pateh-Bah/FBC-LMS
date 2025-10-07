# Secure Keys Rotation Checklist

If any secrets were previously exposed in the repository, rotate them immediately using these steps:

1. Supabase
   - Login to Supabase Dashboard -> Project -> Settings -> API
   - Rotate anon and service_role keys
   - Update the new keys in your deployment platform (Vercel, Render, etc.) and in local `.env` files

2. Database Password
   - Change the database password in Supabase -> Database -> Users
   - Update `DATABASE_URL` in Vercel/GitHub Secrets with the encoded password

3. Vercel
   - Go to Vercel Project -> Settings -> Environment Variables
   - Replace `SECRET_KEY`, `DATABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_ANON_KEY`

4. GitHub
   - Remove any tracked files containing secrets from repo (already done)
   - Rotate any GitHub personal access tokens, if they were exposed
   - Add new secrets to GitHub Actions -> Repository -> Settings -> Secrets

5. Verification
   - Re-run CI security scan (Actions -> Security Scan)
   - Ensure gitleaks pre-commit blocks accidental future commits
   - Confirm no sensitive values are present in code or documentation

6. Communication
   - Inform collaborators to `git fetch origin && git reset --hard origin/main` to sync rewritten history
   - Advise team to delete and re-clone the repository to avoid keeping the old history locally

7. Post-rotation checks
   - Monitor Supabase usage for suspicious activity
   - Check application logs and access patterns for anomalies

If you want, I can prepare exact command-line steps for each provider (Supabase/Vercel) and even automate the Vercel secret update using the Vercel CLI when you provide the new tokens.
