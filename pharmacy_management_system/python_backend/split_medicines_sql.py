#!/usr/bin/env python3
"""
Split the large medicines SQL file into smaller chunks
"""

import os

# Read the original file
input_file = 'supabase_migration/03_data_medicines.sql'
output_dir = 'supabase_migration'

with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Split by the header and data sections
lines = content.split('\n')

# Find where the INSERT statements start
insert_start = -1
for i, line in enumerate(lines):
    if line.strip().startswith('INSERT INTO medicines'):
        insert_start = i
        break

# Get header (everything before INSERT)
header = '\n'.join(lines[:insert_start])

# Get all INSERT lines
insert_lines = []
for i in range(insert_start, len(lines)):
    if lines[i].strip():
        insert_lines.append(lines[i])

print(f"Total lines: {len(lines)}")
print(f"Header lines: {insert_start}")
print(f"Insert lines: {len(insert_lines)}")

# Split into chunks of 1000 records (roughly 2-3 lines per record)
chunk_size = 3000  # characters per chunk, will get roughly 1000 records
chunks = []
current_chunk = []
current_size = 0

for line in insert_lines:
    current_chunk.append(line)
    current_size += len(line) + 1  # +1 for newline
    
    if current_size > chunk_size:
        chunks.append('\n'.join(current_chunk))
        current_chunk = []
        current_size = 0

# Add remaining lines
if current_chunk:
    chunks.append('\n'.join(current_chunk))

print(f"Number of chunks: {len(chunks)}")

# Write chunks to files
for idx, chunk in enumerate(chunks, 1):
    output_file = os.path.join(output_dir, f'03_data_medicines_part{idx}.sql')
    
    # Create header with proper setup
    chunk_content = header.rstrip() + '\n\n' + chunk + '\n'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(chunk_content)
    
    print(f"Created {output_file} ({len(chunk)} bytes)")

print(f"\n✅ Split complete! Created {len(chunks)} files")
print(f"Import them in order: 03_data_medicines_part1.sql, part2.sql, etc.")
