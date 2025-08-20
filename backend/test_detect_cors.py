#!/usr/bin/env python3
"""
Test /detect endpoint CORS specifically
"""

import requests
import time

def test_detect_cors():
    """Test /detect endpoint CORS handling"""
    base_url = "https://artifai.apps.austinjiang.com"
    
    print("🔍 Testing /detect endpoint CORS specifically...")
    print(f"Backend URL: {base_url}")
    print("-" * 50)
    
    # Test 1: OPTIONS preflight
    print("1. Testing OPTIONS preflight...")
    try:
        headers = {
            'Origin': 'https://artifai.austinjiang.com',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Content-Type'
        }
        response = requests.options(f"{base_url}/detect", headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   CORS Origin: {response.headers.get('Access-Control-Allow-Origin')}")
        print(f"   CORS Methods: {response.headers.get('Access-Control-Allow-Methods')}")
        if response.status_code in [200, 204]:
            print("   ✅ OPTIONS preflight working")
        else:
            print("   ❌ OPTIONS preflight failed")
    except Exception as e:
        print(f"   ❌ OPTIONS error: {e}")
    
    print()
    
    # Test 2: POST with small image (should be fast)
    print("2. Testing POST with small image...")
    try:
        headers = {
            'Origin': 'https://artifai.austinjiang.com',
            'Content-Type': 'application/json'
        }
        # Small 1x1 pixel image
        data = {"image": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="}
        
        start_time = time.time()
        response = requests.post(f"{base_url}/detect", json=data, headers=headers, timeout=60)
        end_time = time.time()
        
        print(f"   Status: {response.status_code}")
        print(f"   CORS Origin: {response.headers.get('Access-Control-Allow-Origin')}")
        print(f"   Processing time: {end_time - start_time:.2f} seconds")
        
        if response.status_code == 200:
            print("   ✅ POST request successful")
            result = response.json()
            if 'predictions' in result:
                print(f"   ✅ Got predictions: {result['predictions']}")
        elif response.status_code == 400:
            print("   ⚠️  Got 400 (expected for invalid image)")
        else:
            print(f"   ❌ Unexpected status: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            
    except requests.exceptions.Timeout:
        print("   ❌ Request timed out (>60s)")
    except Exception as e:
        print(f"   ❌ POST error: {e}")
    
    print()
    
    # Test 3: Compare with /query endpoint
    print("3. Testing /query endpoint for comparison...")
    try:
        headers = {
            'Origin': 'https://artifai.austinjiang.com',
            'Content-Type': 'application/json'
        }
        data = [{"role": "user", "content": "Hello"}]
        
        start_time = time.time()
        response = requests.post(f"{base_url}/query", json=data, headers=headers, timeout=30)
        end_time = time.time()
        
        print(f"   Status: {response.status_code}")
        print(f"   CORS Origin: {response.headers.get('Access-Control-Allow-Origin')}")
        print(f"   Processing time: {end_time - start_time:.2f} seconds")
        
        if response.status_code == 200:
            print("   ✅ /query request successful")
        else:
            print(f"   ❌ /query failed: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ /query error: {e}")

if __name__ == "__main__":
    test_detect_cors()
