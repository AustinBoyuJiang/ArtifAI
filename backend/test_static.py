#!/usr/bin/env python3
"""
Test script to verify static file serving
"""

import os
import requests
import time

def test_static_file_serving():
    """Test if static files are accessible"""
    base_url = "https://artifai.apps.austinjiang.com"
    
    # Test endpoints
    endpoints = [
        "/health",
        "/test-static",
        "/public/outlook.png",
        "/public/sitemap.xml"
    ]
    
    print("Testing static file serving...")
    print(f"Base URL: {base_url}")
    print("-" * 50)
    
    for endpoint in endpoints:
        try:
            url = base_url + endpoint
            print(f"Testing: {url}")
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ SUCCESS: {response.status_code}")
                if endpoint.startswith("/public/"):
                    print(f"   Content-Type: {response.headers.get('Content-Type', 'N/A')}")
                    print(f"   Content-Length: {response.headers.get('Content-Length', 'N/A')}")
            else:
                print(f"❌ FAILED: {response.status_code}")
                print(f"   Response: {response.text[:100]}...")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ ERROR: {e}")
        
        print()
        time.sleep(1)  # Small delay between requests

if __name__ == "__main__":
    test_static_file_serving()
