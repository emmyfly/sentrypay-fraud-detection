# SentryPay Demo Instructions

## Quick Start

### 1. Start the API Server (if not running)

```bash
cd sentrypay-backend/api
python main.py
```

The API will start at `http://localhost:8000`

### 2. Open the Demo

Open `sentrypay-demo.html` in your web browser:

- **Option 1:** Double-click the file
- **Option 2:** Right-click → Open with → Your browser
- **Option 3:** Drag and drop into browser window

### 3. Use the Demo

The demo shows:

✅ **Real-time Transaction Feed**
- Live transactions with risk scores from the ML model
- Color-coded by risk level (green=safe, yellow=watch, red=block)

🔍 **Risk Analysis Panel**
- Risk score (0-100) from the trained RandomForest model
- Verdict: safe/watch/block based on thresholds
- Signal breakdown showing feature importances from the actual model
- Transaction details with risk indicators

⚖️ **Resolution Flow**
- For watch/block transactions, choose action:
  - Approve, Flag for Review, or Block

### 4. Simulate Transactions

Click the buttons at the top:

- **Simulate Normal Transaction**: Low risk, safe verdict
- **Simulate Fraud (SIM Swap)**: High amount, recent SIM change, unknown recipient
- **Simulate Suspicious**: Medium risk patterns

### How It Works

The demo uses **real API calls** to `http://localhost:8000/score`:

1. Transaction data is sent as JSON via `fetch()`
2. FastAPI backend loads the trained model
3. Features are extracted using `model/features.py`
4. RandomForest model predicts fraud probability
5. Score converted to 0-100 and verdict assigned
6. Real `feature_importances_` returned as signal breakdown
7. UI updates with actual ML predictions

### API Status Indicator

Top-right corner shows:
- 🟢 **API Connected** - Backend is running
- 🔴 **API Offline** - Start the backend server

### Demo Features

- ✅ Real ML predictions (not hardcoded)
- ✅ Live transaction feed
- ✅ Interactive risk analysis
- ✅ Resolution workflow
- ✅ Transaction history
- ✅ Visual signal breakdown
- ✅ CORS-enabled API calls

### Troubleshooting

**"API Offline" message:**
- Make sure `python main.py` is running in `sentrypay-backend/api/`
- Check that port 8000 is available
- Verify models are trained (model.pkl and mule_model.pkl exist)

**CORS errors:**
- The API has CORS enabled for browser access
- If issues persist, check browser console

**No predictions:**
- Ensure models are trained: `cd model && python train.py`
- Check API logs for errors

## For Judges

This demo showcases:

1. **Real ML Integration**: Live predictions from trained RandomForest model
2. **Feature Engineering**: 18 engineered features including SIM-swap detection
3. **Model Transparency**: Shows actual feature importances from the model
4. **Practical UX**: Transaction feed, risk scoring, and resolution workflow
5. **API Architecture**: Clean separation between ML backend and frontend

The scoring is **100% real** - every prediction comes from the trained model via API call.
