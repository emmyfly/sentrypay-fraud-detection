# 🚀 How to Share Your SentryPay Demo

## ⚡ FASTEST METHOD (5 Minutes)

### Use ngrok to expose your API

**What this does:** Makes your local API accessible from anywhere via a public URL

**Steps:**

1. **Install ngrok** (one time)
```bash
./quick-share.sh
```
It will guide you through setup if needed.

2. **Get your public URL**
When ngrok starts, you'll see:
```
Forwarding  https://abc123-xyz.ngrok.io -> http://localhost:8000
```

3. **Update the demo HTML**
I'll create a version for you - just give me your ngrok URL.

4. **Share with investor**
Send them:
- The updated HTML file
- Tell them to open it in their browser
- It will connect to your API through ngrok!

---

## 📧 ALTERNATIVE: Send Everything as Package

**Steps:**

1. **Run the packaging script:**
```bash
./SHARE_DEMO_NOW.sh
# Choose option 4
```

2. **Upload the file:**
- `sentrypay-demo.tar.gz` will be created
- Upload to Google Drive, Dropbox, or WeTransfer
- Share the link

3. **They follow instructions in the package** to run it locally

---

## 🎥 SIMPLEST: Record a Video

**If you just need to show it quickly:**

1. **Start recording your screen**
```bash
# Press: Ctrl+Shift+Alt+R (Ubuntu built-in)
# Or install: sudo apt install obs-studio
```

2. **Open the demo and show:**
   - Click "Play Scenario Walkthrough"
   - Explain what's happening
   - Show the real-time predictions
   - Explain the ML model

3. **Upload to YouTube (unlisted) or Loom**

4. **Share the video link**

---

## ☁️ PROFESSIONAL: Deploy to Cloud

**For a permanent solution:**

### Option A: Using Render.com (Free)

1. **Create account:** https://render.com
2. **Create New Web Service**
3. **Connect GitHub** (push your code first)
4. Settings:
   - Build: `pip install -r requirements.txt && cd model && python train.py`
   - Start: `cd api && python main.py`
5. **Get your URL:** `https://sentrypay-api.onrender.com`

### Option B: Using Vercel + Railway

**Frontend (HTML):**
- Push to GitHub
- Connect to Vercel
- Auto-deployed!

**Backend (API):**
- Use Railway.app
- Connect GitHub
- One-click deploy

---

## 🎯 My Recommendation

**For TODAY (right now):**
Use **ngrok** - takes 5 minutes, works perfectly

**For THIS WEEK (permanent):**
Deploy to **Render.com** - free tier, always online

**For RIGHT NOW (10 minutes):**
Record a **video** - no setup needed

---

## Step-by-Step: ngrok Method

### 1. Sign up for ngrok (free)
Go to: https://dashboard.ngrok.com/signup

### 2. Get your authtoken
After signup, copy the authtoken from dashboard

### 3. Configure ngrok
```bash
ngrok config add-authtoken YOUR_AUTHTOKEN_HERE
```

### 4. Start the tunnel
```bash
./quick-share.sh
```

You'll see:
```
ngrok                                                      

Session Status                online
Account                       Your Name (Plan: Free)
Forwarding                    https://a1b2-c3d4.ngrok.io -> http://localhost:8000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

### 5. Copy the HTTPS URL
Example: `https://a1b2-c3d4.ngrok.io`

### 6. Tell me that URL
I'll update your demo HTML to use it instead of localhost

### 7. Share the HTML file
Send `sentrypay-investor-demo.html` to your investor
They open it, and it connects to your API through ngrok!

---

## 🔒 Security Note

When using ngrok:
- The free tier URL changes each time you restart
- Anyone with the URL can access your API (during the session)
- Stop ngrok (Ctrl+C) when demo is done

For production, deploy to cloud with proper authentication.

---

## Need Help?

Tell me which method you want to use and I'll help you set it up!
