#!/usr/bin/env python
"""Test out-of-stock endpoint"""

import requests
import json

response = requests.get('http://localhost:5000/api/inventory/out-of-stock')
print(f'Status: {response.status_code}')
data = response.json()

if isinstance(data, list):
    print(f'Found {len(data)} out-of-stock items:\n')
    for item in data:
        med_name = item.get('medicine_name', 'N/A')
        batch_id = item.get('batch_id', 'N/A')
        quantity = item.get('quantity', 'N/A')
        mfg = item.get('manufacturer', 'N/A')
        
        print(f'  • {med_name}')
        print(f'    Batch: {batch_id}')
        print(f'    Quantity: {quantity}')
        print(f'    Manufacturer: {mfg}')
        print()
else:
    print(json.dumps(data, indent=2))
