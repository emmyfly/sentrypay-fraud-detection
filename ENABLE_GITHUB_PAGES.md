# 🌐 Enable GitHub Pages - Quick Guide

Your code is now on GitHub! To share the demo HTML online, enable GitHub Pages:

## Steps (Takes 2 minutes)

### 1. Go to Settings
Open: https://github.com/emmyfly/sentrypay-fraud-detection/settings/pages

### 2. Configure Source
- **Source**: Deploy from a branch
- **Branch**: master
- **Folder**: / (root)
- Click **Save**

### 3. Wait 1-2 minutes
GitHub will build and deploy your site

### 4. Access Your Demo
Once deployed, your demo will be at:

**📱 Investor Demo:**
https://emmyfly.github.io/sentrypay-fraud-detection/sentrypay-investor-demo.html

**🔧 Basic Demo:**
https://emmyfly.github.io/sentrypay-fraud-detection/sentrypay-demo.html

## ⚠️ Important Note

The HTML demos currently point to `http://localhost:8000` for the API.

For the demos to work online, you need to:

### Option A: Use ngrok (Temporary)
1. Start your API locally
2. Run ngrok: `ngrok http 8000`
3. Update the HTML files with your ngrok URL
4. Commit and push changes

### Option B: Deploy API to Cloud (Permanent)
1. Deploy to Render.com, Railway, or Heroku
2. Update HTML files with your deployed API URL
3. Commit and push changes

## Quick Update Script

Want me to create a version that uses your ngrok URL? Just tell me:
1. Your ngrok URL (e.g., https://abc123.ngrok.io)
2. I'll update the HTML and commit

---

✅ **Your repository is live at:**
https://github.com/emmyfly/sentrypay-fraud-detection
