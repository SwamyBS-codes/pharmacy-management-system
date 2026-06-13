#!/usr/bin/env python3
"""Check medicine image URLs in database"""
import requests
import json

BASE_URL = 'http://localhost:5000/api'

print("=" * 80)
print("🖼️ CHECKING MEDICINE IMAGE URLs")
print("=" * 80)

try:
    # Fetch some medicines
    response = requests.get(f"{BASE_URL}/medicines?limit=20", timeout=5)
    
    if response.status_code != 200:
        print(f"❌ Failed to fetch medicines: {response.status_code}")
        exit(1)
    
    data = response.json()
    medicines = data.get('data', [])
    
    print(f"\n📊 Total medicines in response: {len(medicines)}")
    print(f"📊 Database total: {data['pagination']['total']}\n")
    
    # Check image_url presence
    with_image = 0
    without_image = 0
    empty_image = 0
    
    print("Sample medicines (first 10):")
    print("-" * 80)
    
    for i, med in enumerate(medicines[:10]):
        med_id = med.get('id', 'N/A')
        med_name = med.get('medicine_name', 'N/A')
        image_url = med.get('image_url', '')
        
        status = "✓"
        if image_url:
            with_image += 1
            status = "✓ HAS IMAGE"
        elif 'image_url' in med and image_url == '':
            empty_image += 1
            status = "⚠️ EMPTY"
        else:
            without_image += 1
            status = "✗ NULL"
        
        print(f"{i+1}. ID {med_id}: {med_name[:40]}")
        print(f"   {status}")
        if image_url:
            print(f"   URL: {image_url[:60]}...")
        print()
    
    print("-" * 80)
    print(f"\n📈 Summary of all {len(medicines)} medicines:")
    total_with = sum(1 for m in medicines if m.get('image_url'))
    total_without = sum(1 for m in medicines if not m.get('image_url'))
    
    print(f"   ✓ With image_url: {total_with} ({100*total_with//len(medicines) if medicines else 0}%)")
    print(f"   ✗ Without image_url: {total_without} ({100*total_without//len(medicines) if medicines else 0}%)")
    
    print("\n💡 Analysis:")
    if total_without > 0:
        print(f"   ⚠️  {total_without} medicines don't have images")
        print("   → Frontend shows placeholder 'No Image' for these")
        print("   → To add images, edit each medicine and provide an image URL")
    else:
        print("   ✅ All medicines have image URLs!")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("=" * 80)
