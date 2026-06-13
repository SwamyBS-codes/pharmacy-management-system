#!/usr/bin/env python3
"""
Import medicines from model/medicines_with_barcode.csv into the local PostgreSQL database.
"""

import csv
from pathlib import Path
from psycopg2 import extras
from db import get_db_connection, release_db_connection

BASE_DIR = Path(__file__).resolve().parents[2]
CSV_FILE = BASE_DIR / 'model' / 'medicines_with_barcode.csv'

INSERT_SQL = """
INSERT INTO medicines (
    medicine_name,
    composition,
    uses,
    side_effects,
    image_url,
    manufacturer,
    excellent_review_percent,
    average_review_percent,
    poor_review_percent,
    price,
    stock,
    category,
    barcode
) VALUES %s
"""

FIELD_MAP = [
    'Medicine Name',
    'Composition',
    'Uses',
    'Side_effects',
    'Image URL',
    'Manufacturer',
    'Excellent Review %',
    'Average Review %',
    'Poor Review %',
    'barcode_value'
]


def normalize_int(value):
    if value is None:
        return 0
    value = str(value).strip()
    return int(value) if value.isdigit() else 0


def ensure_barcode_column(cursor):
    cursor.execute("ALTER TABLE medicines ADD COLUMN IF NOT EXISTS barcode VARCHAR(255);")


def load_rows():
    if not CSV_FILE.exists():
        raise FileNotFoundError(f"CSV file not found: {CSV_FILE}")

    with CSV_FILE.open(newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = []
        for row in reader:
            medicine_name = row.get('Medicine Name', '').strip()
            if not medicine_name:
                continue
            rows.append(
                (
                    medicine_name,
                    row.get('Composition', '').strip() or None,
                    row.get('Uses', '').strip() or None,
                    row.get('Side_effects', '').strip() or None,
                    row.get('Image URL', '').strip() or None,
                    row.get('Manufacturer', '').strip() or None,
                    normalize_int(row.get('Excellent Review %')),
                    normalize_int(row.get('Average Review %')),
                    normalize_int(row.get('Poor Review %')),
                    0.00,
                    0,
                    None,
                    row.get('barcode_value', '').strip() or None
                )
            )
    return rows


def main():
    print(f"Loading medicines from: {CSV_FILE}")
    rows = load_rows()
    print(f"Found {len(rows)} medicine rows to import.")

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        ensure_barcode_column(cursor)
        extras.execute_values(cursor, INSERT_SQL, rows, template=None, page_size=1000)
        conn.commit()
        cursor.close()

        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM medicines;")
        total_count = cursor.fetchone()[0]
        cursor.close()

        print(f"✅ Imported {len(rows)} rows. Total medicines in database: {total_count}")
    except Exception as e:
        conn.rollback()
        raise
    finally:
        release_db_connection(conn)


if __name__ == '__main__':
    main()
