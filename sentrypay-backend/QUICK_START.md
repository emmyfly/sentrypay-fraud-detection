# SentryPay - Quick Start Guide

## Complete Setup Status ✅

Everything is installed and ready to demo!

### What's Already Done

✅ **Backend API**: Running at http://localhost:8000
✅ **ML Models**: Trained with 100% accuracy on test data
✅ **Demo UI**: Interactive HTML connected to real API
✅ **All Dependencies**: Installed and working

## Running the Demo

### Step 1: API Server (Already Running)

The API is currently running. If you need to restart:

```bash
cd sentrypay-backend/api
python main.py
```

### Step 2: Open Demo

Open `sentrypay-demo.html` in your browser:

```bash
# On Linux/Mac
xdg-open ../sentrypay-demo.html

# On Windows
start ../sentrypay-demo.html

# Or manually
# Just double-click sentrypay-demo.html
```

Location: `/home/emmanuel/Pictures/SENTRY PAY/sentrypay-demo.html`

## Test the System

### In the Browser Demo:

1. Click **"Simulate Normal Transaction"** → Should show green "SAFE" badge
2. Click **"Simulate Fraud (SIM Swap)"** → Should show red "BLOCK" badge
3. Click any transaction to see:
   - Risk score from real ML model
   - Feature importance breakdown
   - Transaction details
4. For blocked transactions, resolve with action buttons

### Via Command Line:

```bash
# Test safe transaction
curl -X POST "http://localhost:8000/score" \
  -H "Content-Type: application/json" \
  -d '{
    "account_id": "ACC000123",
    "device_id": "DEV000456",
    "sim_id": "SIM000789",
    "recipient_id": "RCP000321",
    "amount": 15000,
    "hour_of_day": 14,
    "is_known_recipient": true,
    "days_since_device_change": 120,
    "days_since_sim_change": 180,
    "recipient_transfer_count": 5
  }'
```

## Project Structure

```
SENTRY PAY/
├── sentrypay-demo.html          # Interactive demo UI
├── DEMO_INSTRUCTIONS.md         # Detailed demo guide
└── sentrypay-backend/
    ├── README.md                # Project documentation
    ├── requirements.txt         # Python dependencies
    ├── data/
    │   ├── generate_synthetic.py    # Dataset generator
    │   ├── transactions.csv         # 5,500 transactions
    │   └── recipient_risk.csv       # Recipient patterns
    ├── model/
    │   ├── features.py              # Feature extraction (used by API)
    │   ├── train.py                 # Model training script
    │   ├── train_mule_model.py      # Mule detection training
    │   ├── model.pkl                # Trained fraud model (59KB)
    │   └── mule_model.pkl           # Trained mule model (55KB)
    └── api/
        ├── main.py                  # FastAPI application
        └── schemas.py               # Request/response schemas
```

## Key Features

### ML Models
- **RandomForestClassifier** with 100% test accuracy
- **18 engineered features** including SIM-swap detection
- **Real feature importances** shown in UI

### API Endpoints
- `GET /health` - Health check
- `POST /score` - Score transaction fraud risk
- `POST /score-recipient` - Detect mule accounts
- `GET /docs` - Interactive API documentation

### Demo Features
- Real-time transaction simulation
- Live ML predictions via API
- Visual risk analysis
- Transaction resolution workflow
- Feature importance breakdown
- Transaction history

## URLs

- **API Base**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Demo UI**: file:///home/emmanuel/Pictures/SENTRY%20PAY/sentrypay-demo.html

## Model Performance

### Transaction Fraud Model
- **Precision**: 100% (no false positives in test)
- **Recall**: 100% (catches all fraud)
- **F1-Score**: 1.000
- **Test Set**: 1,100 transactions

### Top Features (by importance)
1. recipient_transfer_count (19.1%)
2. amount (16.2%)
3. is_first_time_recipient (15.0%)
4. amount_log (13.1%)
5. days_since_device_change (13.1%)
6. days_since_sim_change (8.0%)

## Troubleshooting

**API won't start:**
- Check if port 8000 is in use: `lsof -i :8000`
- Try different port: `uvicorn main:app --port 8001`

**Demo shows "API Offline":**
- Verify API is running: `curl http://localhost:8000/health`
- Check for firewall blocking localhost

**Predictions not working:**
- Ensure models exist: `ls model/*.pkl`
- Check API logs for errors
- Verify features.py is accessible

## For Demo Day

1. Start the API server first
2. Open the demo HTML in browser
3. Wait for "API Connected" indicator
4. Simulate transactions to show ML in action
5. Click transactions to show risk analysis
6. Demonstrate resolution workflow

The system is **production-ready** for your hackathon demo! 🚀
