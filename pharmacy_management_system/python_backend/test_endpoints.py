#!/usr/bin/env python
"""Test out-of-stock and predictions endpoints"""

import requests
import json

BASE_URL = 'http://localhost:5000/api'

# Test out-of-stock endpoint
print('Testing Out of Stock Endpoint...')
response = requests.get(f'{BASE_URL}/inventory/out-of-stock')
print(f'Status: {response.status_code}')
if response.status_code == 200:
    data = response.json()
    if isinstance(data, list):
        print(f'Found {len(data)} out of stock items')
        if data:
            print(f'Sample: {json.dumps(data[0], indent=2, default=str)}')
    else:
        print(f'Response: {json.dumps(data, indent=2, default=str)[:500]}')
else:
    print(f'Error: {response.text[:500]}')

print('\n' + '='*80)
print('Testing Predictions Endpoints...')

# Test forecast endpoint
print('\nTesting /predictions/medicine/1/forecast')
response = requests.get(f'{BASE_URL}/predictions/medicine/1/forecast?days=30')
print(f'Status: {response.status_code}')
if response.status_code == 200:
    data = response.json()
    print(f'Response keys: {list(data.keys()) if isinstance(data, dict) else "list"}')
    print(f'Sample: {json.dumps(data, indent=2, default=str)[:500]}')
else:
    print(f'Error: {response.text[:800]}')

# Test reorder-recommendations
print('\nTesting /predictions/reorder-recommendations')
response = requests.get(f'{BASE_URL}/predictions/reorder-recommendations')
print(f'Status: {response.status_code}')
if response.status_code == 200:
    data = response.json()
    data_type = "list" if isinstance(data, list) else "dict"
    if isinstance(data, list):
        print(f'Found {len(data)} reorder recommendations')
        if data:
            print(f'Sample: {json.dumps(data[0], indent=2, default=str)}')
    else:
        print(f'Response: {json.dumps(data, indent=2, default=str)[:500]}')
else:
    print(f'Error: {response.text[:800]}')

# Test seasonal-demand
print('\nTesting /predictions/seasonal-demand')
response = requests.get(f'{BASE_URL}/predictions/seasonal-demand?season=Winter')
print(f'Status: {response.status_code}')
if response.status_code == 200:
    data = response.json()
    data_type = "list" if isinstance(data, list) else "dict"
    if isinstance(data, list):
        print(f'Found {len(data)} seasonal medicines')
        if data:
            print(f'Sample: {json.dumps(data[0], indent=2, default=str)}')
    else:
        print(f'Response: {json.dumps(data, indent=2, default=str)[:500]}')
else:
    print(f'Error: {response.text[:800]}')

# Test expiry-alerts
print('\nTesting /predictions/expiry-alerts')
response = requests.get(f'{BASE_URL}/predictions/expiry-alerts?days=90')
print(f'Status: {response.status_code}')
if response.status_code == 200:
    data = response.json()
    data_type = "list" if isinstance(data, list) else "dict"
    if isinstance(data, list):
        print(f'Found {len(data)} expiry alerts')
        if data:
            print(f'Sample: {json.dumps(data[0], indent=2, default=str)}')
    else:
        print(f'Response: {json.dumps(data, indent=2, default=str)[:500]}')
else:
    print(f'Error: {response.text[:800]}')

# Test sales-analytics
print('\nTesting /predictions/sales-analytics')
response = requests.get(f'{BASE_URL}/predictions/sales-analytics?period=30')
print(f'Status: {response.status_code}')
if response.status_code == 200:
    data = response.json()
    print(f'Response keys: {list(data.keys()) if isinstance(data, dict) else "list"}')
    print(f'Sample: {json.dumps(data, indent=2, default=str)[:500]}')
else:
    print(f'Error: {response.text[:800]}')
