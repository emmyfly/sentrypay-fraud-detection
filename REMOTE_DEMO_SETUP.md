# How to Share SentryPay Demo Remotely

## 🎯 Goal
Allow someone far away to view and interact with your ML-powered fraud detection demo.

## ⚡ Quick Option: Use ngrok (Recommended)

This exposes your local API to the internet temporarily.

### Step 1: Install ngrok
```bash
# Download ngrok
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
tar xvzf ngrok-v3-stable-linux-amd64.tgz
sudo mv ngrok /usr/local/bin/

# Or use snap
sudo snap install ngrok
```

### Step 2: Create ngrok account (free)
1. Go to https://dashboard.ngrok.com/signup
2. Copy your authtoken
3. Run: `ngrok config add-authtoken YOUR_TOKEN`

### Step 3: Expose your API
```bash
# Your API is running on port 8000
ngrok http 8000
```

You'll see output like:
```
Forwarding  https://abc123.ngrok.io -> http://localhost:8000
```

### Step 4: Update demo file
Copy the ngrok URL (e.g., `https://abc123.ngrok.io`) and I'll create a version for you.

---

## 🌐 Option 2: Deploy to Cloud (Production-Ready)

### A. Deploy API to Render.com (Free Tier)

1. **Push code to GitHub**
```bash
cd sentrypay-backend
git init
git add .
git commit -m "Initial commit"
# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/sentrypay-backend.git
git push -u origin main
```

2. **Deploy on Render**
   - Go to https://render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Settings:
     - Name: `sentrypay-api`
     - Environment: `Python 3`
     - Build Command: `pip install -r requirements.txt && cd model && python train.py && python train_mule_model.py`
     - Start Command: `cd api && python main.py`
   - Click "Create Web Service"

3. **Get your API URL**
   - Will be: `https://sentrypay-api.onrender.com`

### B. Deploy API to Railway.app (Easier)

1. Go to https://railway.app
2. Click "Start a New Project"
3. Click "Deploy from GitHub repo"
4. Select `sentrypay-backend`
5. Add environment variables if needed
6. Get your URL: `https://sentrypay-api-production.up.railway.app`

---

## 📤 Option 3: Host Demo HTML on GitHub Pages

### Step 1: Create GitHub repo
```bash
# In the parent directory
git init
git add sentrypay-investor-demo.html
git commit -m "Add investor demo"
# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/sentrypay-demo.git
git push -u origin main
```

### Step 2: Enable GitHub Pages
1. Go to repo Settings → Pages
2. Source: Deploy from branch `main`
3. Save

Your demo will be at: `https://YOUR_USERNAME.github.io/sentrypay-demo/sentrypay-investor-demo.html`

### Step 3: Update API URL in HTML
Before pushing, update the demo to use your deployed API URL.

---

## 🎬 Easiest Solution: Screen Recording

If this is just for one investor meeting:

### Record Demo Video
```bash
# Install screen recorder
sudo apt install simplescreenrecorder

# Or use OBS Studio
sudo apt install obs-studio
```

Record yourself:
1. Opening the demo
2. Clicking "Play Scenario"
3. Explaining what's happening
4. Showing real-time predictions

Upload to:
- YouTube (unlisted)
- Loom
- Google Drive

---

## 🚀 Ready-to-Use Solution (No Setup)

Let me create a version that works with a mock API so you can share immediately.

---

## 📋 What I Recommend

**For immediate sharing (today):**
1. Use ngrok (takes 5 minutes)
2. Share the ngrok URL + investor demo HTML
3. They open the HTML file, it connects to your ngrok URL

**For permanent sharing (this week):**
1. Deploy API to Render.com (free)
2. Host HTML on GitHub Pages (free)
3. Share single URL: `https://yourname.github.io/sentrypay-demo`

**For investor meeting (right now):**
1. Record a 3-minute video
2. Upload to YouTube/Loom
3. Share link

Which approach would you like me to help you set up?
