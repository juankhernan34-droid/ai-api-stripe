#!/bin/bash

# Quick Deployment Script
# Run this to deploy everything at once

echo "🚀 AI API Complete Deployment"
echo "=============================="

# Phase 1: Backend Setup
echo ""
echo "📦 Phase 1: Backend Setup"
echo "Step 1: Navigate to backend"
cd ai-api-stripe || exit

echo "Step 2: Creating .env file"
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ .env created. Please edit with your credentials:"
    echo "  - STRIPE_SECRET_KEY"
    echo "  - STRIPE_PUBLISHABLE_KEY"
    echo "  - STRIPE_STARTER_PRICE_ID"
    echo "  - STRIPE_PRO_PRICE_ID"
    echo "  - PAYPAL_CLIENT_ID"
    echo "  - PAYPAL_CLIENT_SECRET"
    echo "  - HF_TOKEN"
    read -p "Press enter after updating .env"
fi

echo "Step 3: Installing dependencies"
pip install -r requirements.txt

echo ""
echo "✓ Backend setup complete!"

# Phase 2: Mobile Setup
echo ""
echo "📱 Phase 2: Mobile App Setup"
echo "Step 1: Navigate to mobile"
cd ../ai-api-mobile || exit

echo "Step 2: Creating .env file"
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ .env created. Please edit with:"
    echo "  - EXPO_PUBLIC_API_URL"
    echo "  - EXPO_PUBLIC_STRIPE_PUBLISHABLE_KEY"
    echo "  - EXPO_PUBLIC_PAYPAL_CLIENT_ID"
    read -p "Press enter after updating .env"
fi

echo "Step 3: Installing dependencies"
npm install

echo ""
echo "✓ Mobile app setup complete!"

# Phase 3: Testing
echo ""
echo "🧪 Phase 3: Ready to Test"
echo ""
echo "To test locally:"
echo ""
echo "Backend:"
echo "  cd ai-api-stripe"
echo "  python app.py"
echo ""
echo "Mobile (in another terminal):"
echo "  cd ai-api-mobile"
echo "  npm start"
echo "  (press 'w' for web)"
echo ""
echo "=============================="
echo "✅ Setup complete! Ready to deploy."
echo "=============================="
