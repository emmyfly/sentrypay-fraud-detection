#!/bin/bash

echo "🚀 SentryPay Quick Share Setup"
echo "=============================="
echo ""

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "📦 ngrok not found. Installing..."
    
    # Download ngrok
    wget -q --show-progress https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
    tar xzf ngrok-v3-stable-linux-amd64.tgz
    sudo mv ngrok /usr/local/bin/
    rm ngrok-v3-stable-linux-amd64.tgz
    
    echo "✅ ngrok installed!"
    echo ""
fi

# Check if configured
if [ ! -f ~/.ngrok2/ngrok.yml ]; then
    echo "⚙️  ngrok needs configuration"
    echo ""
    echo "Steps:"
    echo "1. Go to: https://dashboard.ngrok.com/get-started/setup"
    echo "2. Sign up (free)"
    echo "3. Copy your authtoken"
    echo "4. Run: ngrok config add-authtoken YOUR_TOKEN"
    echo ""
    echo "Then run this script again!"
    exit 1
fi

# Check if API is running
if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "⚠️  API not running on port 8000"
    echo ""
    echo "Start it with:"
    echo "  cd sentrypay-backend/api"
    echo "  python main.py"
    echo ""
    echo "Then run this script again!"
    exit 1
fi

echo "✅ API is running"
echo "🌐 Starting ngrok tunnel..."
echo ""
echo "This will expose your local API to the internet."
echo "Press Ctrl+C to stop sharing."
echo ""

# Start ngrok
ngrok http 8000
