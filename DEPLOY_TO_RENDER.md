# 🚀 Deploy SentryPay to Render.com (Free)

## Quick Deploy Steps

### 1. Sign up for Render.com
Go to: https://render.com/register

Use your GitHub account for easy integration.

### 2. Create New Web Service

Click: **"New +"** → **"Web Service"**

### 3. Connect GitHub Repository

- Click **"Connect account"** (if first time)
- Select: **emmyfly/sentrypay-fraud-detection**
- Click **"Connect"**

### 4. Configure the Service

**Basic Settings:**
- **Name**: `sentrypay-api`
- **Region**: Oregon (US West) - or closest to you
- **Branch**: `master`
- **Root Directory**: `sentrypay-backend`
- **Environment**: `Python 3`
- **Build Command**:
  ```bash
  pip install -r requirements.txt && python data/generate_synthetic.py && cd model && python train.py && python train_mule_model.py && cd ..
  ```
- **Start Command**:
  ```bash
  cd api && uvicorn main:app --host 0.0.0.0 --port $PORT
  ```

**Plan:**
- Select: **Free** ($0/month)

### 5. Click "Create Web Service"

Render will:
1. Clone your repository
2. Install dependencies (1-2 min)
3. Generate training data
4. Train both ML models (1-2 min)
5. Start the API

Total time: ~5 minutes

### 6. Get Your API URL

Once deployed, you'll see:
```
Your service is live at https://sentrypay-api.onrender.com
```

Copy this URL!

### 7. Test Your Deployed API

```bash
curl https://sentrypay-api.onrender.com/health
```

Should return: `{"status":"ok"}`

---

## Update HTML Demos to Use Deployed API

Once you have your Render URL, I'll update the demo files for you.

Just tell me your URL (e.g., `https://sentrypay-api.onrender.com`)

---

## ⚠️ Important Notes

**Free Tier Limitations:**
- Service "spins down" after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds to wake up
- 750 hours/month free (enough for demos)

**For Production:**
- Upgrade to paid plan ($7/month) for always-on
- Or use Railway.app, Heroku, or AWS

---

## Alternative: Railway.app (Easier)

Railway is even simpler:

1. Go to: https://railway.app
2. Click: "Start a New Project"
3. "Deploy from GitHub repo"
4. Select: `sentrypay-fraud-detection`
5. Railway auto-detects Python and deploys!

Your URL: `https://sentrypay-api-production.up.railway.app`

---

## After Deployment

Once you have your API URL, we'll:
1. ✅ Update demo HTML files
2. ✅ Enable GitHub Pages  
3. ✅ Share link: `https://emmyfly.github.io/sentrypay-fraud-detection/sentrypay-investor-demo.html`

Anyone can then view and interact with your ML demo!
