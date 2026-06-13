#!/usr/bin/env python3
"""Find medicines without images"""
import requests

BASE_URL = 'http://localhost:5000/api'

print("🔍 Finding medicines WITHOUT images...\n")

try:
    # Fetch more medicines to find ones without images
    for page in range(1, 50):  # Check first 50 pages
        response = requests.get(f"{BASE_URL}/medicines?limit=100&page={page}", timeout=5)
        
        if response.status_code != 200:
            break
        
        data = response.json()
        medicines = data.get('data', [])
        
        if not medicines:
            break
        
        # Find ones without images
        missing = [m for m in medicines if not m.get('image_url')]
        
        if missing:
            print(f"❌ Found {len(missing)} medicines without images on page {page}:")
            for med in missing[:5]:  # Show first 5
                print(f"   ID {med['id']}: {med['medicine_name']}")
            
            if len(missing) > 5:
                print(f"   ... and {len(missing) - 5} more")
            break
    else:
        print("✅ All medicines checked have images!")
        
except Exception as e:
    print(f"Error: {e}")
