#!/usr/bin/env python
"""Simple test to fetch and inspect existing sale"""

import requests
import json

BASE_URL = "http://localhost:5000/api"

# Get the first sale
response = requests.get(f"{BASE_URL}/sales")
print(f"Sales fetch status: {response.status_code}")
sales = response.json()
print(f"Sales response type: {type(sales)}")
print(f"First few sales:")

if isinstance(sales, dict):
    data = sales.get('data', [])
elif isinstance(sales, list):
    data = sales
else:
    data = []

for sale in data[:2]:
    print(f"\n{json.dumps(sale, indent=2, default=str)}")
    
    # Try to get invoice for this sale
    sale_id = sale.get('id')
    print(f"\n--- Attempting to generate invoice for sale {sale_id} ---")
    
    # Check if sale exists
    check_response = requests.get(f"{BASE_URL}/sales/{sale_id}")
    print(f"Sale check status: {check_response.status_code}")
    if check_response.status_code == 200:
        print(f"Sale detail: {json.dumps(check_response.json(), indent=2, default=str)}")
    else:
        print(f"Error checking sale: {check_response.text}")
    
    # Try to generate invoice
    gen_response = requests.post(f"{BASE_URL}/billing/generate-invoice/{sale_id}")
    print(f"Invoice generation status: {gen_response.status_code}")
    print(f"Response: {json.dumps(gen_response.json(), indent=2, default=str)}")
