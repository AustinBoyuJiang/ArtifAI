#!/bin/bash

echo "🚀 Deploying and testing CORS fix..."
echo "====================================="

# Deploy to production
echo "📦 Deploying to production..."
./deploy.sh

echo ""
echo "⏳ Waiting for deployment to complete..."
sleep 30

echo ""
echo "🧪 Testing CORS configuration..."
python3 quick_cors_test.py

echo ""
echo "✅ Deployment and testing completed!"
echo "🔗 Frontend: https://artifai.austinjiang.com"
echo "🔗 Backend: https://artifai.apps.austinjiang.com"
