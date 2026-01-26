#!/usr/bin/env python3
import requests
import json
import time

time.sleep(2)  # Give server time to start

BASE_URL = 'http://localhost:5000'

endpoints = [
    ('GET', '/api/inventory/out-of-stock', 'Out of Stock'),
    ('GET', '/api/predictions/medicine/1/forecast?days=30', 'Forecast'),
    ('GET', '/api/predictions/seasonal-demand?season=Winter&limit=5', 'Seasonal Demand'),
    ('GET', '/api/predictions/reorder-recommendations', 'Reorder Recommendations'),
    ('GET', '/api/predictions/expiry-alerts?days=90', 'Expiry Alerts'),
    ('GET', '/api/predictions/sales-analytics?period=30', 'Sales Analytics'),
]

print('Testing Predictions Endpoints:')
print('='*60)

for method, path, name in endpoints:
    try:
        url = BASE_URL + path
        r = requests.get(url, timeout=5)
        print(f'✓ {name}: {r.status_code}')
        
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, list):
                print(f'  └─ {len(data)} items')
            elif isinstance(data, dict):
                print(f'  └─ Keys: {list(data.keys())[:5]}')
    except Exception as e:
        print(f'✗ {name}: {str(e)[:50]}')

print('='*60)
print('Testing Complete')
