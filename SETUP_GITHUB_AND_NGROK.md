# 🚀 Setup Guide: GitHub + ngrok

## ✅ Git Repository - ALREADY DONE!

Your code is now in a Git repository. Here's what's next:

### Push to GitHub

1. **Create a new repository on GitHub:**
   - Go to: https://github.com/new
   - Name it: `sentrypay-fraud-detection`
   - Don't initialize with README (we already have files)
   - Click "Create repository"

2. **Link your local repo to GitHub:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/sentrypay-fraud-detection.git
   git branch -M main
   git push -u origin main
   ```

3. **Done!** Your code is now on GitHub

---

## 🌐 ngrok Setup - FOR QUICK SHARING

### What is ngrok?
It creates a public URL that tunnels to your local API (localhost:8000)

**Example:**
- Your API: `http://localhost:8000`
- After ngrok: `https://abc123.ngrok.io`
- Anyone can access it!

### Step-by-Step Setup

#### 1. Install ngrok
```bash
# Download
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz

# Extract
tar xvzf ngrok-v3-stable-linux-amd64.tgz

# Move to system path
sudo mv ngrok /usr/local/bin/

# Clean up
rm ngrok-v3-stable-linux-amd64.tgz
```

#### 2. Sign up for ngrok (FREE)
- Go to: https://dashboard.ngrok.com/signup
- Sign up with your email
- You'll get an authtoken

#### 3. Configure ngrok with your token
```bash
ngrok config add-authtoken YOUR_AUTHTOKEN_HERE
```
(Replace `YOUR_AUTHTOKEN_HERE` with your actual token from the dashboard)

#### 4. Start ngrok tunnel
```bash
# Make sure your API is running first
# In one terminal:
cd sentrypay-backend/api
python main.py

# In another terminal:
ngrok http 8000
```

#### 5. You'll see something like this:
```
ngrok                                                                           

Session Status                online
Account                       Your Name (Plan: Free)
Forwarding                    https://a1b2-c3d4.ngrok.io -> http://localhost:8000

Web Interface                 http://127.0.0.1:4040
```

#### 6. Copy your public URL
Example: `https://a1b2-c3d4.ngrok.io`

#### 7. Update the demo HTML
Tell me your ngrok URL and I'll create a version of the demo that uses it!

Or manually edit `sentrypay-investor-demo.html`:
- Find: `const API_URL = 'http://localhost:8000';`
- Replace with: `const API_URL = 'https://YOUR-NGROK-URL.ngrok.io';`

#### 8. Share the HTML file
Send `sentrypay-investor-demo.html` to your investor
They open it in their browser, and it connects to your API!

---

## 📤 How to Share with Someone

### Option A: Send HTML file directly
1. Start ngrok (step 4 above)
2. Update HTML with ngrok URL (step 7)
3. Email/send the HTML file
4. They open it in their browser - works!

### Option B: Host HTML online
1. Push to GitHub (already done)
2. Go to your repo settings
3. Enable GitHub Pages
4. Share URL: `https://YOUR_USERNAME.github.io/sentrypay-fraud-detection/sentrypay-investor-demo.html`

---

## 🎯 Quick Commands Summary

```bash
# 1. Push to GitHub (one time)
git remote add origin https://github.com/YOUR_USERNAME/sentrypay-fraud-detection.git
git branch -M main
git push -u origin main

# 2. Install ngrok (one time)
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
tar xvzf ngrok-v3-stable-linux-amd64.tgz
sudo mv ngrok /usr/local/bin/
rm ngrok-v3-stable-linux-amd64.tgz

# 3. Configure ngrok (one time)
ngrok config add-authtoken YOUR_TOKEN

# 4. Every time you want to share:
# Terminal 1:
cd sentrypay-backend/api && python main.py

# Terminal 2:
ngrok http 8000
```

---

## ❓ What to Do Next

Tell me:
1. Do you want to push to GitHub now?
2. Do you want me to help install ngrok?
3. Do you have an ngrok URL I should use to update the HTML?

I'll help you with whichever you need!
