import requests
import json

BASE_URL = "http://localhost:5000/api/suppliers"


def main():
    # Create a new supplier
    payload = {
        "name": "Test Supplier",
        "email": "supplier@example.com",
        "contact": "+91-99999-00000",
        "address": "123 Pharma Street, MedCity"
    }
    print("Creating supplier...")
    r = requests.post(BASE_URL, json=payload)
    print("Status:", r.status_code)
    try:
        data = r.json()
    except Exception:
        print("Response text:", r.text)
        return
    print("Response:", json.dumps(data, indent=2))

    if r.status_code not in (200, 201):
        print("Failed to create supplier")
        return

    # List suppliers
    print("\nListing suppliers...")
    r2 = requests.get(BASE_URL)
    print("Status:", r2.status_code)
    try:
        data2 = r2.json()
    except Exception:
        print("Response text:", r2.text)
        return
    print("Count:", len(data2) if isinstance(data2, list) else data2)
    print("Sample (first 3):", json.dumps(data2[:3], indent=2) if isinstance(data2, list) else data2)


if __name__ == "__main__":
    main()
