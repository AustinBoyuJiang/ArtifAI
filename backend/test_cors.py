#!/usr/bin/env python3
"""
Test script to verify CORS configuration
"""

import requests
import json

def test_cors_configuration():
    """Test CORS configuration for the backend"""
    base_url = "https://artifai.apps.austinjiang.com"
    
    # Test endpoints
    test_cases = [
        {
            "name": "Health Check",
            "url": f"{base_url}/health",
            "method": "GET",
            "headers": {
                "Origin": "https://artifai.austinjiang.com",
                "Content-Type": "application/json"
            }
        },
        {
            "name": "Detect Endpoint (OPTIONS preflight)",
            "url": f"{base_url}/detect",
            "method": "OPTIONS",
            "headers": {
                "Origin": "https://artifai.austinjiang.com",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type"
            }
        },
        {
            "name": "Query Endpoint (OPTIONS preflight)",
            "url": f"{base_url}/query",
            "method": "OPTIONS",
            "headers": {
                "Origin": "https://artifai.austinjiang.com",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type"
            }
        }
    ]
    
    print("Testing CORS configuration...")
    print(f"Base URL: {base_url}")
    print("-" * 60)
    
    for test_case in test_cases:
        try:
            print(f"Testing: {test_case['name']}")
            print(f"URL: {test_case['url']}")
            print(f"Method: {test_case['method']}")
            
            if test_case['method'] == 'OPTIONS':
                response = requests.options(test_case['url'], headers=test_case['headers'], timeout=10)
            else:
                response = requests.get(test_case['url'], headers=test_case['headers'], timeout=10)
            
            print(f"Status Code: {response.status_code}")
            
            # Check CORS headers
            cors_headers = {
                'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
                'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
                'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
                'Access-Control-Allow-Credentials': response.headers.get('Access-Control-Allow-Credentials')
            }
            
            print("CORS Headers:")
            for header, value in cors_headers.items():
                print(f"  {header}: {value}")
            
            if response.status_code in [200, 204]:
                print("✅ SUCCESS")
            else:
                print("❌ FAILED")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ ERROR: {e}")
        
        print("-" * 60)
        print()

def test_actual_request():
    """Test an actual POST request to see if CORS works"""
    base_url = "https://artifai.apps.austinjiang.com"
    
    print("Testing actual POST request...")
    print(f"URL: {base_url}/detect")
    
    # Test data (minimal)
    test_data = {
        "image": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="  # 1x1 pixel PNG
    }
    
    headers = {
        "Origin": "https://artifai.austinjiang.com",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            f"{base_url}/detect",
            json=test_data,
            headers=headers,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin')}")
        
        if response.status_code == 200:
            print("✅ CORS POST request successful")
        else:
            print(f"❌ Request failed: {response.text[:200]}...")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_cors_configuration()
    print("\n" + "="*60 + "\n")
    test_actual_request()
