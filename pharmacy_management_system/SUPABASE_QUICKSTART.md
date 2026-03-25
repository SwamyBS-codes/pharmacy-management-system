# 🚀 Supabase Quick Deployment - TL;DR

## Prerequisites
1. Create Supabase account at https://supabase.com
2. Create a new project in Supabase dashboard
3. Note your database password

## Quick Start (5 minutes)

### Option 1: Automated Deployment (Recommended)

```powershell
# Run the deployment wizard
.\deploy-to-supabase.ps1
```

The wizard will:
- ✅ Export your local database
- ✅ Create configuration files
- ✅ Import to Supabase
- ✅ Verify the migration

### Option 2: Manual Steps

```powershell
cd python_backend

# 1. Export data
python export_data_for_supabase.py

# 2. Get Supabase connection details
# Go to Supabase → Settings → Database → Connection string

# 3. Create .env.supabase
# Copy .env.supabase.example and fill in your details

# 4. Import to Supabase (choose one):

# A) Automatic import
python import_to_supabase.py

# B) Manual via Supabase SQL Editor
# Upload files from supabase_migration/ folder in order

# 5. Verify
python verify_supabase_migration.py
```

## Supabase Connection Details

Find in: **Supabase Dashboard → Settings → Database**

```env
DB_HOST=db.xxxxx.supabase.co
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres.xxxxx
DB_PASSWORD=your-password
```

## Update Your Application

Edit `python_backend/.env`:

```env
DB_HOST=db.xxxxx.supabase.co
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres.xxxxx
DB_PASSWORD=your-password
```

## Test

```powershell
# Start backend
cd python_backend
python app.py

# Start frontend (new terminal)
npm run dev
```

## Files Created

| File | Purpose |
|------|---------|
| `deploy-to-supabase.ps1` | One-click deployment wizard |
| `python_backend/export_data_for_supabase.py` | Export local data to SQL files |
| `python_backend/import_to_supabase.py` | Import SQL files to Supabase |
| `python_backend/verify_supabase_migration.py` | Verify migration success |
| `python_backend/.env.supabase.example` | Template for Supabase config |
| `SUPABASE_DEPLOYMENT_GUIDE.md` | Detailed documentation |

## Common Issues

### ❌ Connection timeout
- Check firewall settings
- Verify Supabase project is active (not paused)

### ❌ Import fails
- Import files in correct order (01, 02, 03...)
- Check for special characters in data

### ❌ Slow queries
- Use connection pooling (port 6543)
- Update DB_HOST to `db.xxxxx.pooler.supabase.com`
- Update DB_PORT to `6543`

## Security Checklist

- [ ] Change SECRET_KEY in .env
- [ ] Use strong database password
- [ ] Enable Row Level Security in Supabase
- [ ] Never commit .env.supabase to Git
- [ ] Use connection pooling in production

## Production Settings

For production, use connection pooling:

```env
DB_HOST=db.xxxxx.pooler.supabase.com
DB_PORT=6543
DB_NAME=postgres
DB_USER=postgres.xxxxx
DB_PASSWORD=your-password
DEBUG=False
```

## Monitoring

Monitor in Supabase Dashboard:
- **Database → Logs** - Query logs
- **Database → Reports** - Performance metrics
- **Settings → Billing** - Usage stats

## Backup Strategy

Supabase provides automatic daily backups. For manual backups:

```powershell
# Export current state
python export_data_for_supabase.py
```

Keep exports versioned for rollback capability.

## Need Help?

- 📚 Full Guide: [SUPABASE_DEPLOYMENT_GUIDE.md](SUPABASE_DEPLOYMENT_GUIDE.md)
- 🌐 Supabase Docs: https://supabase.com/docs
- 💬 Supabase Discord: https://discord.supabase.com

---

**Ready to deploy? Run:** `.\deploy-to-supabase.ps1`
