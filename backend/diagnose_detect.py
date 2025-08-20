#!/usr/bin/env python3
"""
Diagnose /detect endpoint issues
"""

import requests
import base64
import json

def test_detect_components():
    """Test different components of the detect endpoint"""
    base_url = "https://artifai.apps.austinjiang.com"
    
    print("🔍 Diagnosing /detect endpoint issues...")
    print(f"Backend URL: {base_url}")
    print("-" * 50)
    
    # Test 1: Basic connectivity
    print("1. Testing basic connectivity...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("   ✅ Backend is reachable")
        else:
            print(f"   ❌ Backend returned {response.status_code}")
    except Exception as e:
        print(f"   ❌ Cannot reach backend: {e}")
        return
    
    print()
    
    # Test 2: OPTIONS preflight
    print("2. Testing OPTIONS preflight...")
    try:
        headers = {
            'Origin': 'https://artifai.austinjiang.com',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Content-Type'
        }
        response = requests.options(f"{base_url}/detect", headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   CORS Origin: {response.headers.get('Access-Control-Allow-Origin')}")
        if response.status_code in [200, 204]:
            print("   ✅ OPTIONS preflight working")
        else:
            print("   ❌ OPTIONS preflight failed")
    except Exception as e:
        print(f"   ❌ OPTIONS error: {e}")
    
    print()
    
    # Test 3: Simple POST with minimal data
    print("3. Testing POST with minimal data...")
    try:
        headers = {
            'Origin': 'https://artifai.austinjiang.com',
            'Content-Type': 'application/json'
        }
        data = {"image": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="}  # 1x1 pixel
        response = requests.post(f"{base_url}/detect", json=data, headers=headers, timeout=30)
        print(f"   Status: {response.status_code}")
        print(f"   CORS Origin: {response.headers.get('Access-Control-Allow-Origin')}")
        
        if response.status_code == 200:
            print("   ✅ POST request successful")
            result = response.json()
            if 'predictions' in result:
                print(f"   ✅ Got predictions: {result['predictions']}")
            if 'heatmap' in result:
                print(f"   ✅ Got heatmap (length: {len(result['heatmap'])})")
        elif response.status_code == 400:
            print("   ⚠️  Got 400 (expected for invalid image)")
            print(f"   Response: {response.text[:200]}...")
        else:
            print(f"   ❌ Unexpected status: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            
    except Exception as e:
        print(f"   ❌ POST error: {e}")
    
    print()
    
    # Test 4: Test with larger image
    print("4. Testing with larger image...")
    try:
        # Create a larger test image (10x10 pixels)
        larger_image = "iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyJpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuMy1jMDExIDY2LjE0NTY2MSwgMjAxMi8wMi8wNi0xNDo1NjoyNyAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENTNiAoV2luZG93cykiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6QjY0NjdGNjM4RTU0MTFFQ0E1NUNGRTY1NkRCMzMyMkIiIHhtcE1NOkRvY3VtZW50SUQ9InhtcC5kaWQ6QjY0NjdGNjQ4RTU0MTFFQ0E1NUNGRTY1NkRCMzMyMkIiPiA8eG1wTU06RGVyaXZlZEZyb20gc3RSZWY6aW5zdGFuY2VJRD0ieG1wLmlpZDpCNjQ2N0Y2MThFNTQxMUVDQTU1Q0ZFNjU2REIzMzIyQiIgc3RSZWY6ZG9jdW1lbnRJRD0ieG1wLmRpZDpCNjQ2N0Y2MjhFNTQxMUVDQTU1Q0ZFNjU2REIzMzIyQiIvPiA8L3JkZjpEZXNjcmlwdGlvbj4gPC9yZGY6UkRGPiA8L3g6eG1wbWV0YT4gPD94cGFja2V0IGVuZD0iciI/PgH//v38+/r5+Pf29fTz8vHw7+7t7Ovq6ejn5uXk4+Lh4N/e3dzb2tnY19bV1NPS0dDPzs3My8rJyMfGxcTDwsHAv769vLu6ubi3trW0s7KxsK+urayrqqmop6alpKOioaCfnp2cm5qZmJeWlZSTkpGQj46NjIuKiYiHhoWEg4KBgH9+fXx7enl4d3Z1dHNycXBvbm1sa2ppaGdmZWRjYmFgX15dXFtaWVhXVlVUU1JRUE9OTUxLSklIR0ZFRENCQUA/Pj08Ozo5ODc2NTQzMjEwLy4tLCsqKSgnJiUkIyIhIB8eHRwbGhkYFxYVFBMSERAPDg0MCwoJCAcGBQQDAgEAACH5BAEAAAAALAAAAAAoACgAAAIRhI+py+0Po5y02ouz3rz7D4biSJbmiabqyrbuCwAAOw=="
        
        headers = {
            'Origin': 'https://artifai.austinjiang.com',
            'Content-Type': 'application/json'
        }
        data = {"image": larger_image}
        response = requests.post(f"{base_url}/detect", json=data, headers=headers, timeout=60)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Larger image processed successfully")
        else:
            print(f"   ❌ Failed with status: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_detect_components()
