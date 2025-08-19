#!/bin/bash

echo "🔧 Testing CORS fix for ArtifAI..."
echo "=================================="

# Test CORS configuration
echo "📋 Testing CORS headers..."
python3 backend/test_cors.py

echo ""
echo "🌐 Testing static file access..."
python3 backend/test_static.py

echo ""
echo "✅ CORS fix test completed!"
echo "If you see ✅ SUCCESS messages above, the CORS issue should be resolved."
echo ""
echo "🔗 You can now test the frontend at: https://artifai.austinjiang.com"
echo "🔗 Backend API at: https://artifai.apps.austinjiang.com"
