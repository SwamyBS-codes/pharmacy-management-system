#!/usr/bin/env python3
import requests
import json

# Test the invoice generation endpoint
BASE_URL = "http://localhost:5000/api"

try:
    # Check health
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health check: {response.json()}")
    
    # List invoices to see what sales exist
    response = requests.get(f"{BASE_URL}/billing/invoices")
    print(f"\nExisting sales: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Found {len(data.get('data', []))} invoices")
        if data.get('data'):
            for invoice in data['data'][:3]:
                print(f"  - Sale ID: {invoice['id']}, Invoice #: {invoice['invoice_number']}")
            
            # Test generating invoice for the first sale
            first_sale_id = data['data'][0]['id']
            print(f"\n--- Testing Invoice Generation for Sale ID: {first_sale_id} ---")
            
            # Generate invoice
            gen_response = requests.post(f"{BASE_URL}/billing/generate-invoice/{first_sale_id}")
            print(f"Generate invoice response ({gen_response.status_code}):")
            if gen_response.status_code in [200, 201]:
                print(json.dumps(gen_response.json(), indent=2))
                print("\n✅ Invoice generated successfully!")
                
                # Preview invoice data
                print(f"\n--- Preview Invoice ---")
                preview_response = requests.get(f"{BASE_URL}/billing/invoice/{first_sale_id}/preview")
                if preview_response.status_code == 200:
                    preview_data = preview_response.json()
                    print(f"Invoice Number: {preview_data.get('invoice_number')}")
                    print(f"Customer: {preview_data.get('customer_name')} - {preview_data.get('customer_phone')}")
                    print(f"Pharmacy: {preview_data.get('pharmacy', {}).get('pharmacy_name')}")
                    print(f"Total: Rs. {preview_data.get('final_amount')}")
                    print(f"Items: {len(preview_data.get('items', []))}")
                    for i, item in enumerate(preview_data.get('items', [])[:3], 1):
                        print(f"  {i}. {item.get('medicine_name')} - Batch: {item.get('batch_id')} - Qty: {item.get('quantity')}")
            else:
                print(f"Error: {gen_response.text}")
    else:
        print(f"Error: {response.text}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
