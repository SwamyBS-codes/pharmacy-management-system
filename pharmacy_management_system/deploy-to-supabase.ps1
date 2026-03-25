# Supabase Deployment Wizard for Pharmacy Management System

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Supabase Deployment Wizard" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "python_backend")) {
    Write-Host "Error: Please run this from the project root directory" -ForegroundColor Red
    exit 1
}

Set-Location python_backend

# Step 1: Check if local database is accessible
Write-Host "Step 1: Checking local database connection..." -ForegroundColor Yellow
$env:PYTHONIOENCODING = "utf-8"
python -c "from config import Config; import psycopg2; psycopg2.connect(**Config.get_db_connection_string()).close(); print('Local database connected')" 2>$null

if ($LASTEXITCODE -ne 0) {
    Write-Host "Cannot connect to local database!" -ForegroundColor Red
    Write-Host "Please ensure your local PostgreSQL is running." -ForegroundColor Yellow
    exit 1
}

# Step 2: Export data
Write-Host ""
Write-Host "Step 2: Exporting data from local database..." -ForegroundColor Yellow
python export_data_for_supabase.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "Export failed!" -ForegroundColor Red
    exit 1
}

# Step 3: Setup Supabase environment
Write-Host ""
Write-Host "Step 3: Supabase configuration..." -ForegroundColor Yellow

if (-not (Test-Path ".env.supabase")) {
    Write-Host "Creating .env.supabase file..." -ForegroundColor Cyan
    Copy-Item ".env.supabase.example" ".env.supabase"
    Write-Host ""
    Write-Host "IMPORTANT: Please edit .env.supabase with your Supabase details:" -ForegroundColor Yellow
    Write-Host "   1. Go to https://app.supabase.com" -ForegroundColor White
    Write-Host "   2. Create a new project (if you haven't already)" -ForegroundColor White
    Write-Host "   3. Go to Settings -> Database" -ForegroundColor White
    Write-Host "   4. Copy your connection details to .env.supabase" -ForegroundColor White
    Write-Host ""
    
    $continue = Read-Host "Have you updated .env.supabase? (yes/no)"
    if ($continue -ne "yes") {
        Write-Host "Please update .env.supabase and run this script again." -ForegroundColor Yellow
        exit 0
    }
} else {
    Write-Host "Found existing .env.supabase" -ForegroundColor Green
}

# Step 4: Import to Supabase
Write-Host ""
Write-Host "Step 4: Ready to import to Supabase!" -ForegroundColor Yellow
Write-Host ""
Write-Host "You have two options:" -ForegroundColor Cyan
Write-Host "  A) Automatic import using Python script" -ForegroundColor White
Write-Host "  B) Manual import via Supabase SQL Editor" -ForegroundColor White
Write-Host ""
$choice = Read-Host "Choose option (A/B)"

if ($choice -eq "A" -or $choice -eq "a") {
    Write-Host ""
    Write-Host "Starting automatic import..." -ForegroundColor Yellow
    python import_to_supabase.py
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "Step 5: Verifying migration..." -ForegroundColor Yellow
        python verify_supabase_migration.py
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "=====================================" -ForegroundColor Green
            Write-Host "DEPLOYMENT SUCCESSFUL!" -ForegroundColor Green
            Write-Host "=====================================" -ForegroundColor Green
            Write-Host ""
            Write-Host "Next steps:" -ForegroundColor Cyan
            Write-Host "1. Update your main .env file with Supabase details" -ForegroundColor White
            Write-Host "2. Test your application: python app.py" -ForegroundColor White
            Write-Host ""
        }
    }
} else {
    Write-Host ""
    Write-Host "Manual Import Instructions:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "1. Go to your Supabase project dashboard" -ForegroundColor White
    Write-Host "2. Click SQL Editor in the left sidebar" -ForegroundColor White
    Write-Host "3. Create a new query" -ForegroundColor White
    Write-Host "4. Copy contents from supabase_migration/ files and run them in order:" -ForegroundColor White
    Write-Host "   - 01_schema.sql" -ForegroundColor Yellow
    Write-Host "   - 02_data_core.sql" -ForegroundColor Yellow
    Write-Host "   - 03_data_medicines.sql" -ForegroundColor Yellow
    Write-Host "   - 04_data_inventory.sql" -ForegroundColor Yellow
    Write-Host "   - 05_data_customers.sql" -ForegroundColor Yellow
    Write-Host "   - 06_data_sales.sql" -ForegroundColor Yellow
    Write-Host "   - 07_data_other.sql" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "5. After manual import, run verification:" -ForegroundColor White
    Write-Host "   python verify_supabase_migration.py" -ForegroundColor Yellow
    Write-Host ""
}

Write-Host ""
Write-Host "For detailed documentation, see: SUPABASE_DEPLOYMENT_GUIDE.md" -ForegroundColor Cyan
Write-Host ""

Set-Location ..
