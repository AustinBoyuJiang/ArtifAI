#!/usr/bin/env python3
"""
Quick CORS test
"""

import requests

def quick_test():
    url = "https://artifai.apps.austinjiang.com/detect"
    
    print("🚀 Quick CORS Test")
    print(f"Testing: {url}")
    print("-" * 40)
    
    # Test OPTIONS
    print("1. Testing OPTIONS preflight...")
    try:
        headers = {
            'Origin': 'https://artifai.austinjiang.com',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Content-Type'
        }
        response = requests.options(url, headers=headers, timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   CORS Origin: {response.headers.get('Access-Control-Allow-Origin')}")
        print(f"   CORS Methods: {response.headers.get('Access-Control-Allow-Methods')}")
        if response.status_code in [200, 204]:
            print("   ✅ OPTIONS working")
        else:
            print("   ❌ OPTIONS failed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test POST
    print("2. Testing POST request...")
    try:
        headers = {
            'Origin': 'https://artifai.austinjiang.com',
            'Content-Type': 'application/json'
        }
        data = {"test": "data"}
        response = requests.post(url, json=data, headers=headers, timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   CORS Origin: {response.headers.get('Access-Control-Allow-Origin')}")
        if response.status_code == 400:  # Expected for invalid request
            print("   ✅ POST working (got 400 as expected)")
        else:
            print(f"   ⚠️  Got status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    quick_test()
