#!/bin/bash

echo "═══════════════════════════════════════════════════════════"
echo "   🚀 SHARE SENTRYPAY DEMO - QUICK SETUP"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Choose your sharing method:"
echo ""
echo "1. 🔗 Use ngrok (expose local API to internet)"
echo "   → Best for: Live demo with real ML"
echo "   → Setup time: 5 minutes"
echo "   → They get: Working demo with your API"
echo ""
echo "2. 📹 Record video (screen recording)"
echo "   → Best for: Quick sharing, no setup"
echo "   → Setup time: 10 minutes"
echo "   → They get: Video of you demoing"
echo ""
echo "3. ☁️  Deploy to cloud (permanent hosting)"
echo "   → Best for: Professional presentation"
echo "   → Setup time: 20 minutes"
echo "   → They get: Permanent URL"
echo ""
echo "4. 📧 Send files + instructions"
echo "   → Best for: Technical audience"
echo "   → Setup time: 2 minutes"
echo "   → They get: Files to run locally"
echo ""
read -p "Enter choice (1-4): " choice

case $choice in
  1)
    echo ""
    echo "📦 Installing ngrok..."
    if ! command -v ngrok &> /dev/null; then
        echo "Downloading ngrok..."
        wget -q https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
        tar xzf ngrok-v3-stable-linux-amd64.tgz
        sudo mv ngrok /usr/local/bin/
        rm ngrok-v3-stable-linux-amd64.tgz
        echo "✅ ngrok installed"
    else
        echo "✅ ngrok already installed"
    fi
    
    echo ""
    echo "📝 Setup instructions:"
    echo "1. Sign up at: https://dashboard.ngrok.com/signup"
    echo "2. Copy your authtoken"
    echo "3. Run: ngrok config add-authtoken YOUR_TOKEN"
    echo "4. Run: ngrok http 8000"
    echo "5. Copy the https URL (e.g., https://abc123.ngrok.io)"
    echo "6. Send that URL + sentrypay-investor-demo.html to your investor"
    echo ""
    echo "Need help? Run: ./configure-ngrok.sh"
    ;;
    
  2)
    echo ""
    echo "📹 Screen Recording Options:"
    echo ""
    echo "Option A: SimpleScreenRecorder (Linux)"
    echo "  sudo apt install simplescreenrecorder"
    echo "  Launch it and record your demo"
    echo ""
    echo "Option B: OBS Studio (All platforms)"
    echo "  sudo apt install obs-studio"
    echo "  Professional recording with overlays"
    echo ""
    echo "Option C: Browser built-in (Chrome/Edge)"
    echo "  1. Open demo in browser"
    echo "  2. Press Ctrl+Shift+P (Chrome) or F12 (Dev tools)"
    echo "  3. Search 'Record' → Start recording"
    echo ""
    echo "📤 After recording, upload to:"
    echo "  • YouTube (unlisted) - https://youtube.com/upload"
    echo "  • Loom - https://loom.com"
    echo "  • Google Drive - share the link"
    ;;
    
  3)
    echo ""
    echo "☁️  Cloud Deployment Steps:"
    echo ""
    echo "STEP 1: Push to GitHub"
    echo "------------------------"
    echo "cd sentrypay-backend"
    echo "git init"
    echo "git add ."
    echo "git commit -m 'Initial commit'"
    echo "# Create repo at github.com, then:"
    echo "git remote add origin https://github.com/YOUR_USERNAME/sentrypay.git"
    echo "git push -u origin main"
    echo ""
    echo "STEP 2: Deploy API to Render.com"
    echo "--------------------------------"
    echo "1. Go to https://render.com/deploy"
    echo "2. Connect GitHub"
    echo "3. Select sentrypay-backend repo"
    echo "4. Build: pip install -r requirements.txt"
    echo "5. Start: cd api && python main.py"
    echo "6. Copy your URL: https://sentrypay-api.onrender.com"
    echo ""
    echo "STEP 3: Update demo HTML"
    echo "-----------------------"
    echo "Replace 'http://localhost:8000' with your Render URL"
    echo ""
    echo "STEP 4: Host HTML on GitHub Pages"
    echo "---------------------------------"
    echo "1. Push HTML to GitHub"
    echo "2. Settings → Pages → Enable"
    echo "3. Share: https://yourname.github.io/sentrypay-demo"
    ;;
    
  4)
    echo ""
    echo "📧 Preparing files to send..."
    
    # Create a shareable package
    mkdir -p sentrypay-share
    cp sentrypay-investor-demo.html sentrypay-share/
    cp INVESTOR_DEMO_README.md sentrypay-share/
    cp -r sentrypay-backend sentrypay-share/
    
    cat > sentrypay-share/SETUP_INSTRUCTIONS.txt << 'EOF'
SENTRYPAY DEMO - SETUP INSTRUCTIONS
====================================

This is a complete ML-powered fraud detection demo.

PREREQUISITES:
- Python 3.8+
- pip

SETUP (5 minutes):

1. Open Terminal/Command Prompt

2. Navigate to the folder:
   cd sentrypay-share/sentrypay-backend

3. Install dependencies:
   pip install pandas numpy scikit-learn fastapi uvicorn pydantic

4. Generate data and train models:
   python data/generate_synthetic.py
   cd model
   python train.py
   python train_mule_model.py

5. Start the API:
   cd ../api
   python main.py

6. Open the demo:
   Double-click sentrypay-investor-demo.html
   
7. Click "Play Scenario Walkthrough"

The demo uses real machine learning to detect fraud in real-time.

TROUBLESHOOTING:
- If "API Offline" appears, make sure step 5 is running
- API runs at: http://localhost:8000
- Check API: curl http://localhost:8000/health

Questions? Contact: [YOUR EMAIL]
EOF
    
    # Create archive
    tar -czf sentrypay-demo.tar.gz sentrypay-share/
    
    echo "✅ Package created: sentrypay-demo.tar.gz"
    echo ""
    echo "📧 Send this file + SETUP_INSTRUCTIONS.txt to your investor"
    echo ""
    echo "Or upload to:"
    echo "  • Google Drive: share link"
    echo "  • Dropbox: share link"
    echo "  • WeTransfer: wetransfer.com"
    ;;
    
  *)
    echo "Invalid choice"
    ;;
esac

echo ""
echo "═══════════════════════════════════════════════════════════"
