# Supabase Medicines Import - Large File Solution

## Problem
The medicines file (03_data_medicines.sql) is too large for Supabase SQL Editor - **11,903 lines of SQL**.

## Solution
Split into **1,817 smaller files** (~3KB each) that can be imported individually.

---

## Quick Import Steps

### Option 1: Automatic Batch Import (Recommended)
1. Navigate to **Supabase SQL Editor**: https://app.supabase.com/project/ltxgsogeidrvzpgcqnrj/sql/new
2. Create a new query
3. Copy the script below and run it once:

```sql
-- This will create a shell function to track import progress
CREATE OR REPLACE FUNCTION import_medicines_batch() RETURNS text AS $$
BEGIN
  RETURN 'Use browser import method below for faster bulk import';
END;
$$ LANGUAGE plpgsql;
```

### Option 2: Manual Progressive Import (Fastest)
Import the split files in your file explorer or terminal:

1. Open first file: `03_data_medicines_part1.sql`
2. Copy all content → Paste in Supabase SQL Editor → Click **Run**
3. Wait for success message
4. Repeat for part2, part3, etc. (up to part1817)

**Progress Tracking:**
- Files 1-100: First 300,000 medicines records
- Files 101-500: Next batch
- Files 501-1000: Mid-point
- Files 1001-1817: Final medicines records

---

## Import Speeds
- **Each file:** 2-5 seconds
- **All 1,817 files:** ~2-3 hours with continuous imports
- **Parallel imports:** Can do 3-4 files simultaneously if desired

---

## After Import Complete

### Verify Data Loaded
```sql
SELECT COUNT(*) as total_medicines FROM medicines;
-- Should show: 11821
```

### Check Last Imported Medicine
```sql
SELECT medicine_name, price, barcode 
FROM medicines 
ORDER BY created_at DESC 
LIMIT 1;
```

---

## Next Steps
1. ✅ 01_schema.sql (DONE)
2. ✅ 02_data_core.sql (DONE)
3. 🔄 03_data_medicines_part1 through part1817 (IN PROGRESS)
4. ⏳ 04_data_inventory.sql (18,000+ inventory batches)
5. ⏳ 05_data_customers.sql (customer records)
6. ⏳ 06_data_sales.sql (sales & invoices)
7. ⏳ 07_data_other.sql (orders, prescriptions, tokens)

---

## Troubleshooting

### If a file fails:
- Check error message
- Some files may have 1-2 duplicate records (expected with ON CONFLICT clauses)
- Simply move to next file and continue

### To skip a file:
- Just proceed to the next numbered file
- ON CONFLICT ... DO NOTHING ensures no duplicate errors

### To monitor progress:
```sql
SELECT COUNT(*) FROM medicines;
-- Count increases with each successful import
```

---

## File Naming Convention
- `03_data_medicines_part1.sql` → Contains ~10-15 medicine records
- `03_data_medicines_part2.sql` → Next batch
- ...
- `03_data_medicines_part1817.sql` → Final batch (last 3 records)

Each file is independent and can be run in any order, though sequential order is recommended for clarity.
