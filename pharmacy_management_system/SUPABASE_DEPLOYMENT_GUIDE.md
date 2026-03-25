# 🚀 Supabase Deployment Guide

This guide will help you deploy your pharmacy management system database to Supabase.

## 📋 Prerequisites

- A Supabase account (sign up at https://supabase.com)
- Your local PostgreSQL database with data
- Python installed with psycopg2

## 🔧 Step-by-Step Deployment

### Step 1: Create a Supabase Project

1. Go to https://app.supabase.com
2. Click "New Project"
3. Fill in:
   - **Name**: pharmacy-management-system
   - **Database Password**: (Choose a strong password and save it!)
   - **Region**: Choose closest to your location
4. Wait for the project to be created (~2 minutes)

### Step 2: Get Your Supabase Connection Details

1. In your Supabase project dashboard, go to **Settings** → **Database**
2. Scroll down to **Connection string** → **URI**
3. Copy the connection string (looks like: `postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres`)
4. Note down these details:
   - **Host**: `db.xxxxx.supabase.co`
   - **Port**: `5432`
   - **Database**: `postgres`
   - **User**: `postgres.xxxxx`
   - **Password**: (Your database password)

### Step 3: Create Environment Configuration

Create a new file `.env.supabase` in your `python_backend` folder:

```env
# Supabase Database Configuration
DB_HOST=db.xxxxx.supabase.co
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres.xxxxx
DB_PASSWORD=your-database-password

# Other settings
SECRET_KEY=your-secret-key-change-this
DEBUG=False
PYTHON_PORT=5000
HOST=0.0.0.0
```

Replace the values with your actual Supabase connection details.

### Step 4: Export Your Local Data

Run the export script to create SQL dumps of your data:

```powershell
cd python_backend
python export_data_for_supabase.py
```

This will create:
- `supabase_migration/01_schema.sql` - Database schema
- `supabase_migration/02_data_medicines.sql` - Medicines data
- `supabase_migration/03_data_other.sql` - Other tables data

### Step 5: Deploy Schema to Supabase

1. Go to your Supabase project dashboard
2. Click on **SQL Editor** in the left sidebar
3. Click **New Query**
4. Open `supabase_migration/01_schema.sql` and copy its contents
5. Paste into the SQL editor and click **Run**
6. Wait for completion (should show success message)

### Step 6: Import Your Data

#### Option A: Using Supabase SQL Editor (Recommended for small datasets)

1. In **SQL Editor**, create a new query
2. Open `supabase_migration/02_data_medicines.sql`
3. Copy and paste the contents
4. Click **Run**
5. Repeat for `supabase_migration/03_data_other.sql`

#### Option B: Using Python Script (Recommended for large datasets)

```powershell
python import_to_supabase.py
```

This will:
- Connect to your Supabase database
- Import all data from the SQL files
- Show progress and confirm completion

### Step 7: Verify the Migration

Run the verification script:

```powershell
python verify_supabase_migration.py
```

This will check:
- ✅ All tables exist
- ✅ Data counts match
- ✅ Indexes are created
- ✅ Constraints are active

### Step 8: Update Your Application Configuration

#### For Development:

Create a `.env` file in `python_backend`:

```env
# Use Supabase
DB_HOST=db.xxxxx.supabase.co
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres.xxxxx
DB_PASSWORD=your-database-password

SECRET_KEY=your-secret-key
DEBUG=True
PYTHON_PORT=5000
HOST=0.0.0.0
```

#### For Production:

Set these environment variables in your hosting platform:
- `DB_HOST`
- `DB_PORT`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `SECRET_KEY`
- `DEBUG=False`

### Step 9: Test Your Application

1. Start your backend:
   ```powershell
   cd python_backend
   python app.py
   ```

2. Start your frontend:
   ```powershell
   cd ..
   npm run dev
   ```

3. Test the application:
   - Login with your admin account
   - Check if medicines load
   - Try creating a sale
   - Verify inventory updates

## 🔒 Security Best Practices

### 1. Enable Row Level Security (RLS)

In Supabase SQL Editor, run:

```sql
-- Enable RLS on all tables
ALTER TABLE pharmacy ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE medicines ENABLE ROW LEVEL SECURITY;
ALTER TABLE inventory ENABLE ROW LEVEL SECURITY;
ALTER TABLE suppliers ENABLE ROW LEVEL SECURITY;
ALTER TABLE customers ENABLE ROW LEVEL SECURITY;
ALTER TABLE sales ENABLE ROW LEVEL SECURITY;
ALTER TABLE sales_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE prescriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE auth_tokens ENABLE ROW LEVEL SECURITY;

-- Create policies (your backend handles auth, so allow service role)
-- These policies allow authenticated access through your backend
```

### 2. Use Connection Pooling

For production, use Supabase's connection pooling:
- In Supabase dashboard → Settings → Database
- Use the **Connection Pooling** connection string
- Update `DB_PORT` to `6543` (pooling port)
- Update `DB_HOST` to include `.pooler.supabase.com`

### 3. Secure Your API Keys

- Never commit `.env` files to Git
- Use environment variables in production
- Rotate your database password regularly

## 🎯 Post-Deployment Checklist

- [ ] Schema deployed successfully
- [ ] All data migrated
- [ ] Verification script passes
- [ ] Application connects to Supabase
- [ ] Login/authentication works
- [ ] Sales/POS functionality works
- [ ] Inventory updates correctly
- [ ] Reports generate properly
- [ ] Backup strategy in place

## 🔄 Continuous Deployment

### Database Backups

Supabase automatically backs up your database. You can also:

1. Use Supabase's backup feature (Settings → Database → Backups)
2. Schedule manual exports:
   ```powershell
   python export_data_for_supabase.py
   ```

### Schema Changes

For future schema updates:

1. Create migration files in `supabase_migration/migrations/`
2. Test locally first
3. Apply to Supabase via SQL Editor
4. Version control your migration files

## 🆘 Troubleshooting

### Connection Timeout
- Check your firewall settings
- Verify Supabase project is not paused
- Ensure connection string is correct

### Import Fails
- Check data format (especially dates and decimals)
- Verify foreign key constraints
- Import in order: schema → medicines → inventory → sales

### Slow Queries
- Use connection pooling (port 6543)
- Add indexes for frequently queried columns
- Use Supabase's query performance tools

## 📊 Monitoring

Monitor your Supabase database:
1. Go to **Database** → **Logs** for query logs
2. Check **Database** → **Reports** for performance metrics
3. Set up alerts for high connection usage

## 🔗 Useful Links

- [Supabase Documentation](https://supabase.com/docs)
- [Supabase Python Client](https://github.com/supabase-community/supabase-py)
- [PostgreSQL Connection Pooling](https://supabase.com/docs/guides/database/connecting-to-postgres#connection-pool)

---

**Need Help?** Check the Supabase community forum or Discord for support.
