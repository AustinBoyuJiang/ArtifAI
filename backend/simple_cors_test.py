#!/usr/bin/env python3
"""
Simple CORS test script
"""

import requests

def test_cors():
    base_url = "https://artifai.apps.austinjiang.com"
    
    print("🔧 Testing CORS configuration...")
    print(f"Backend URL: {base_url}")
    print(f"Frontend Origin: https://artifai.austinjiang.com")
    print("-" * 50)
    
    # Test 1: Health endpoint
    print("1. Testing /health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   CORS Origin: {response.headers.get('Access-Control-Allow-Origin', 'NOT SET')}")
        if response.status_code == 200:
            print("   ✅ Health endpoint working")
        else:
            print("   ❌ Health endpoint failed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test 2: OPTIONS preflight for /detect
    print("2. Testing OPTIONS preflight for /detect...")
    try:
        headers = {
            'Origin': 'https://artifai.austinjiang.com',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Content-Type'
        }
        response = requests.options(f"{base_url}/detect", headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   CORS Origin: {response.headers.get('Access-Control-Allow-Origin', 'NOT SET')}")
        print(f"   CORS Methods: {response.headers.get('Access-Control-Allow-Methods', 'NOT SET')}")
        print(f"   CORS Headers: {response.headers.get('Access-Control-Allow-Headers', 'NOT SET')}")
        if response.status_code in [200, 204]:
            print("   ✅ OPTIONS preflight working")
        else:
            print("   ❌ OPTIONS preflight failed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test 3: Simple POST request
    print("3. Testing simple POST request...")
    try:
        headers = {
            'Origin': 'https://artifai.austinjiang.com',
            'Content-Type': 'application/json'
        }
        data = {"test": "data"}
        response = requests.post(f"{base_url}/detect", json=data, headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   CORS Origin: {response.headers.get('Access-Control-Allow-Origin', 'NOT SET')}")
        if response.status_code == 400:  # Expected for invalid request
            print("   ✅ POST request working (got expected 400)")
        else:
            print(f"   ⚠️  Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_cors()
