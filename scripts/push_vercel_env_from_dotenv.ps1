<#
PowerShell helper: push_vercel_env_from_dotenv.ps1
Reads a .env file at project root and pushes a selected set of variables to Vercel using the Vercel CLI.

USAGE:
  1. Install and login to Vercel CLI: `vercel login`
  2. From project root run: .\scripts\push_vercel_env_from_dotenv.ps1 -Environment production
  3. Confirm prompts to push each variable.

SECURITY:
 - This script reads secrets from your local .env (which should be gitignored). It will transmit secrets to Vercel; run only on a secure machine.
 - The script will NOT commit or print secrets to repo files.
#>
param(
    [ValidateSet('production','preview','development')]
    [string]$Environment = 'production',

    [switch]$PushPublicOnly  # If set, only push NEXT_PUBLIC_ variables
)

$envFile = Join-Path $PSScriptRoot '..' -ChildPath '.env'
if (-not (Test-Path $envFile)) {
    Write-Error "Could not find .env at $envFile. Create it first and ensure it contains the variables to push."
    exit 1
}

# Variables we will push by default. Add/remove as desired.
$varsToPush = @(
    'SECRET_KEY',
    'DEBUG',
    'DJANGO_SETTINGS_MODULE',
    'DATABASE_URL',
    # Supabase variables removed from automatic push
    'ALLOWED_HOSTS',
    'ANNUAL_SUBSCRIPTION_FEE',
    'FINE_PER_DAY'
)

$publicVars = @(
    # No public Supabase variables to push
)

if ($PushPublicOnly) {
    $varsToPush = $publicVars
} else {
    # Append public vars so they are set too
    $varsToPush += $publicVars
}

# Parse .env into a dict
$lines = Get-Content $envFile | Where-Object { $_ -and -not $_.TrimStart().StartsWith('#') }
$envDict = @{}
foreach ($line in $lines) {
    if ($line -match '^\s*([^=\s]+)\s*=\s*(.*)\s*$') {
        $k = $matches[1]
        $v = $matches[2]
        # Strip surrounding quotes if present
        if ($v.StartsWith('"') -and $v.EndsWith('"')) { $v = $v.Substring(1,$v.Length-2) }
        if ($v.StartsWith("'") -and $v.EndsWith("'")) { $v = $v.Substring(1,$v.Length-2) }
        $envDict[$k] = $v
    }
}

# Confirm Vercel CLI available
try {
    $vercelVersion = & vercel --version 2>$null
} catch {
    Write-Error "Vercel CLI not found in PATH. Install and login: npm i -g vercel; vercel login"
    exit 1
}

Write-Host "Pushing environment variables to Vercel ($Environment)"

foreach ($var in $varsToPush) {
    if (-not $envDict.ContainsKey($var)) {
        Write-Warning "$var not found in .env; skipping."
        continue
    }

    $value = $envDict[$var]

    # Ask confirmation for server-only secret vars
    if ($var -eq 'SUPABASE_SERVICE_ROLE_KEY' -or $var -eq 'SECRET_KEY' -or $var -eq 'DATABASE_URL') {
        $confirm = Read-Host "Push $var to Vercel ($Environment)? This will upload a secret. Type 'yes' to continue"
        if ($confirm -ne 'yes') {
            Write-Warning "Skipped $var"
            continue
        }
    }

    # Use vercel env add <name> <value> <environment>
    Write-Host "Setting $var..."
    # Build command and execute
    $cmd = "vercel env add $var \"$value\" $Environment"
    Write-Host "Executing: $cmd"
    try {
        iex $cmd
        Write-Host "Set $var ($Environment)"
    } catch {
        Write-Error "Failed to set $var: $_"
    }
}

Write-Host "Done. Verify variables in Vercel Dashboard or using 'vercel env list'."
