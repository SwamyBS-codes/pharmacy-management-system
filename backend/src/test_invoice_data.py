#!/usr/bin/env python
"""Test script to verify invoice PDF generation with real data"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000/api"

# Test 1: Check if sales exist
print("=" * 60)
print("CHECKING EXISTING SALES")
print("=" * 60)

response = requests.get(f"{BASE_URL}/sales", headers={"Authorization": "Bearer test"})
print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Found {len(data.get('data', []))} sales")
    if data.get('data'):
        sale = data['data'][0]
        print(f"Sample sale: {json.dumps(sale, indent=2, default=str)}")
        print(f"\nGenerating invoice for sale ID: {sale['id']}")
        
        # Generate invoice
        inv_response = requests.post(
            f"{BASE_URL}/generate-invoice/{sale['id']}"
        )
        print(f"Invoice generation status: {inv_response.status_code}")
        if inv_response.status_code == 200:
            print(f"Response: {json.dumps(inv_response.json(), indent=2)}")
else:
    print(f"Error: {response.text}")

print("\n" + "=" * 60)
print("CREATING TEST SALE DATA")
print("=" * 60)

# First, get existing pharmacy
pharmacy_response = requests.get(f"{BASE_URL}/auth/me")
print(f"Auth check: {pharmacy_response.status_code}")

# Create test customer
customer_data = {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "9876543210",
    "address": "123 Main Street"
}

customer_response = requests.post(
    f"{BASE_URL}/customers",
    json=customer_data
)
print(f"Customer creation: {customer_response.status_code}")
if customer_response.status_code == 201:
    customer = customer_response.json()
    print(f"Customer created: {json.dumps(customer, indent=2, default=str)}")
    customer_id = customer.get('data', {}).get('id', customer.get('id'))
else:
    print(f"Error: {customer_response.text}")
    customer_id = 1

# Get medicines with inventory
medicines_response = requests.get(f"{BASE_URL}/medicines")
print(f"Medicines fetch: {medicines_response.status_code}")
medicines = medicines_response.json().get('data', [])[:3]
print(f"Found {len(medicines)} medicines")

# Check inventory
inventory_response = requests.get(f"{BASE_URL}/inventory")
print(f"Inventory fetch: {inventory_response.status_code}")
inventory_items = inventory_response.json().get('data', [])
print(f"Found {len(inventory_items)} inventory items")

# Create sale
sale_items = []
for i, medicine in enumerate(medicines[:2]):
    inv_item = next((item for item in inventory_items if item.get('medicine_id') == medicine.get('id')), None)
    if inv_item:
        sale_items.append({
            "medicine_id": medicine.get('id'),
            "inventory_id": inv_item.get('id'),
            "quantity": 2,
            "unit_price": 150.00
        })

sale_data = {
    "customer_id": customer_id,
    "items": sale_items,
    "payment_method": "cash",
    "discount_amount": 0,
    "sold_by": 1
}

print(f"\nSale data to create: {json.dumps(sale_data, indent=2)}")

sale_response = requests.post(
    f"{BASE_URL}/sales",
    json=sale_data
)
print(f"Sale creation: {sale_response.status_code}")
if sale_response.status_code == 201:
    new_sale = sale_response.json()
    print(f"Sale created: {json.dumps(new_sale, indent=2, default=str)}")
    sale_id = new_sale.get('data', {}).get('id', new_sale.get('id'))
    
    print(f"\nGenerating invoice for new sale ID: {sale_id}")
    inv_response = requests.post(
        f"{BASE_URL}/generate-invoice/{sale_id}"
    )
    print(f"Invoice generation status: {inv_response.status_code}")
    if inv_response.status_code == 200:
        print(f"Response: {json.dumps(inv_response.json(), indent=2)}")
    else:
        print(f"Error: {inv_response.text}")
else:
    print(f"Error: {sale_response.text}")
