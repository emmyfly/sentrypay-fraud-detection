# SentryPay Backend - Fraud Detection System

Real-time fraud detection API for bank transactions using machine learning.

## Project Structure

```
sentrypay-backend/
├── data/
│   └── generate_synthetic.py    # Generate synthetic training data
├── model/
│   ├── features.py              # Feature extraction (reusable for API)
│   ├── train.py                 # Train fraud detection model
│   └── train_mule_model.py      # Train mule account detection model
├── api/
│   ├── main.py                  # FastAPI application
│   └── schemas.py               # Request/response models
└── requirements.txt             # Python dependencies
```

## Setup Instructions

### 1. Install Dependencies

```bash
cd sentrypay-backend
pip install -r requirements.txt
```

If you have connection issues, install individually:
```bash
pip install pandas numpy scikit-learn fastapi uvicorn pydantic
```

### 2. Generate Training Data

```bash
python data/generate_synthetic.py
```

This creates:
- `data/transactions.csv` - 5,500 transactions (5,000 normal, 500 fraud)
- `data/recipient_risk.csv` - Recipient patterns for mule detection

### 3. Train Models

```bash
cd model
python train.py              # Trains fraud detection model → model.pkl
python train_mule_model.py   # Trains mule detection model → mule_model.pkl
cd ..
```

### 4. Start API Server

```bash
cd api
python main.py
```

Or with auto-reload for development:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- OpenAPI Spec: http://localhost:8000/openapi.json

## API Endpoints

### GET /health
Health check endpoint.

```bash
curl http://localhost:8000/health
```

### POST /score
Score a transaction for fraud risk.

```bash
curl -X POST "http://localhost:8000/score" \
  -H "Content-Type: application/json" \
  -d '{
    "account_id": "ACC000123",
    "device_id": "DEV000456",
    "sim_id": "SIM000789",
    "recipient_id": "RCP000321",
    "amount": 15000.00,
    "hour_of_day": 14,
    "is_known_recipient": true,
    "days_since_device_change": 120,
    "days_since_sim_change": 180,
    "recipient_transfer_count": 5
  }'
```

Response:
```json
{
  "score": 23,
  "verdict": "safe",
  "signal_breakdown": {
    "days_since_sim_change": 0.25,
    "amount": 0.18,
    "is_known_recipient": 0.15
  }
}
```

Verdicts:
- **safe** (score < 35): Low risk, allow transaction
- **watch** (35 ≤ score < 65): Medium risk, flag for review
- **block** (score ≥ 65): High risk, block transaction

### POST /score-recipient
Check if a recipient account shows mule account patterns.

```bash
curl -X POST "http://localhost:8000/score-recipient" \
  -H "Content-Type: application/json" \
  -d '{
    "recipient_id": "RCP000100",
    "num_transactions": 25,
    "avg_amount": 8500.00,
    "days_span": 90,
    "unique_senders_30d": 5,
    "first_time_senders_30d": 1
  }'
```

## Features

### Transaction Fraud Detection
- **SIM-swap detection**: Flags recent device/SIM changes
- **Amount analysis**: High-value transfers to unknown recipients
- **Time patterns**: Unusual transaction hours
- **Recipient familiarity**: First-time vs known recipients

### Mule Account Detection
- **Sender diversity**: Many unique first-time senders
- **Velocity patterns**: High transaction volume in short timeframe
- **Amount patterns**: Large average amounts from unfamiliar sources

## Model Performance

Run training scripts to see detailed metrics:
- Precision, Recall, F1-Score
- Confusion Matrix (false positives/negatives)
- Feature Importance Rankings

## Development

The project is structured for hackathon judges:
- Clean, readable code
- Clear separation of concerns
- Reusable feature extraction
- Comprehensive evaluation metrics

## Tech Stack

- **FastAPI**: Modern Python web framework
- **scikit-learn**: RandomForestClassifier for fraud detection
- **pandas/numpy**: Data processing
- **Pydantic**: Request/response validation
- **uvicorn**: ASGI server
