# Manual Supabase Deployment via SQL Editor

Since direct database connection is timing out (likely due to firewall/network restrictions), use Supabase's built-in SQL Editor instead.

## Steps

### 1. Go to Your Supabase Project
1. Open https://app.supabase.com
2. Click on your project: "pharmacy-management-system"

### 2. Open SQL Editor
1. Click **"SQL Editor"** in the left sidebar
2. Click **"New Query"**

### 3. Import Schema
1. Open file: `python_backend/supabase_migration/01_schema.sql`
2. Copy ALL the contents
3. Paste into the SQL Editor in Supabase
4. Click **"Run"** button (or press Ctrl+Enter)
5. Wait for completion (should see "Success" message)

### 4. Import Data Files (in order)
Repeat step 3 for each file:

```
1. 01_schema.sql        (COMPLETED)
2. 02_data_core.sql
3. 03_data_medicines.sql
4. 04_data_inventory.sql
5. 05_data_customers.sql
6. 06_data_sales.sql
7. 07_data_other.sql
```

For each file:
1. Create a new query in SQL Editor
2. Copy file contents
3. Run
4. Check for "Success" message

### 5. Files Location
All files are in:
```
python_backend/supabase_migration/
```

## Expected Data After Import

- ✅ 1 Pharmacy
- ✅ 3 Users (Admin + 2 Employees)
- ✅ 11,821 Medicines
- ✅ 3 Suppliers
- ✅ 3 Inventory batches
- ✅ 10 Customers
- ✅ 69 Sales
- ✅ 30 Sale items

## After Import

Once all files are imported:

1. Update your main `.env` file:
   ```env
   DB_HOST=db.ltxgsogeidrvzpgcqnrj.supabase.co
   DB_PORT=5432
   DB_NAME=postgres
   DB_USER=postgres.ltxgsogeidrvzpgcqnrj
   DB_PASSWORD=Swamybs@#321
   ```

2. Test your application:
   ```powershell
   python app.py
   ```

3. Open browser to http://localhost:5000

## Tips

- Each query in SQL Editor has a 10-minute timeout
- If a query times out, split it into smaller parts
- Check the "Results" tab to see output
- Use "Format" button to clean up SQL if needed

## Troubleshooting

**Query times out?**
- The data files might be too large
- Try importing the smaller data files first (02, 04, 05, 07)
- Then import 03_data_medicines.sql and 06_data_sales.sql separately

**Foreign key errors?**
- Make sure you run files in the correct order
- Run 01_schema.sql first, then 02_data_core.sql before other data files

**Duplicate key errors?**
- Clear all tables first by running: `DROP SCHEMA public CASCADE; CREATE SCHEMA public;`
- Then re-run 01_schema.sql

Good luck! 🚀
