"""
FastAPI backend for SentryPay fraud detection.
"""
import sys
import os
import pickle
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Add parent directory to path to import from model/
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from model.features import extract_features, extract_recipient_features
from api.schemas import (
    TransactionRequest, 
    RecipientRiskRequest, 
    RiskResponse, 
    HealthResponse
)

# Initialize FastAPI app
app = FastAPI(
    title="SentryPay Fraud Detection API",
    description="Real-time fraud detection for bank transactions using ML",
    version="1.0.0"
)

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for loaded models
fraud_model = None
fraud_feature_names = None
mule_model = None
mule_feature_names = None


@app.on_event("startup")
async def load_models():
    """Load ML models at startup."""
    global fraud_model, fraud_feature_names, mule_model, mule_feature_names
    
    # Load fraud detection model
    fraud_model_path = os.path.join(os.path.dirname(__file__), '..', 'model', 'model.pkl')
    try:
        with open(fraud_model_path, 'rb') as f:
            fraud_data = pickle.load(f)
            fraud_model = fraud_data['model']
            fraud_feature_names = fraud_data['feature_names']
        print(f"✓ Loaded fraud detection model from {fraud_model_path}")
    except FileNotFoundError:
        print(f"⚠ Warning: Fraud model not found at {fraud_model_path}")
        print("  Run 'python model/train.py' to train the model first")
    
    # Load mule account detection model
    mule_model_path = os.path.join(os.path.dirname(__file__), '..', 'model', 'mule_model.pkl')
    try:
        with open(mule_model_path, 'rb') as f:
            mule_data = pickle.load(f)
            mule_model = mule_data['model']
            mule_feature_names = mule_data['feature_names']
        print(f"✓ Loaded mule detection model from {mule_model_path}")
    except FileNotFoundError:
        print(f"⚠ Warning: Mule model not found at {mule_model_path}")
        print("  Run 'python model/train_mule_model.py' to train the model first")


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint to confirm server is running."""
    return {"status": "ok"}


@app.post("/score", response_model=RiskResponse)
async def score_transaction(transaction: TransactionRequest):
    """
    Score a transaction for fraud risk.
    
    Returns a risk score (0-100) and verdict:
    - score >= 65: "block" (high fraud risk)
    - score >= 35: "watch" (medium risk, flag for review)
    - score < 35: "safe" (low risk)
    """
    if fraud_model is None:
        raise HTTPException(
            status_code=503,
            detail="Fraud detection model not loaded. Train the model first with 'python model/train.py'"
        )
    
    # Convert request to dict and extract features
    transaction_dict = transaction.model_dump()
    features = extract_features(transaction_dict)
    
    # Ensure features are in correct order
    feature_values = [features[name] for name in fraud_feature_names]
    
    # Get fraud probability from model
    fraud_probability = fraud_model.predict_proba([feature_values])[0][1]
    
    # Convert to 0-100 score
    score = int(round(fraud_probability * 100))
    
    # Apply thresholds
    if score >= 65:
        verdict = "block"
    elif score >= 35:
        verdict = "watch"
    else:
        verdict = "safe"
    
    # Get feature importances from model
    signal_breakdown = {
        name: float(importance) 
        for name, importance in zip(fraud_feature_names, fraud_model.feature_importances_)
    }
    
    # Sort by importance (descending)
    signal_breakdown = dict(sorted(signal_breakdown.items(), key=lambda x: x[1], reverse=True))
    
    return {
        "score": score,
        "verdict": verdict,
        "signal_breakdown": signal_breakdown
    }


@app.post("/score-recipient", response_model=RiskResponse)
async def score_recipient(recipient: RecipientRiskRequest):
    """
    Score a recipient account for mule account risk.
    
    Returns a risk score (0-100) and verdict:
    - score >= 65: "block" (likely mule account)
    - score >= 35: "watch" (suspicious pattern)
    - score < 35: "safe" (normal recipient)
    """
    if mule_model is None:
        raise HTTPException(
            status_code=503,
            detail="Mule detection model not loaded. Train the model first with 'python model/train_mule_model.py'"
        )
    
    # Convert request to dict and extract features
    recipient_dict = recipient.model_dump()
    features = extract_recipient_features(recipient_dict)
    
    # Ensure features are in correct order
    feature_values = [features[name] for name in mule_feature_names]
    
    # Get mule probability from model
    mule_probability = mule_model.predict_proba([feature_values])[0][1]
    
    # Convert to 0-100 score
    score = int(round(mule_probability * 100))
    
    # Apply thresholds
    if score >= 65:
        verdict = "block"
    elif score >= 35:
        verdict = "watch"
    else:
        verdict = "safe"
    
    # Get feature importances from model
    signal_breakdown = {
        name: float(importance) 
        for name, importance in zip(mule_feature_names, mule_model.feature_importances_)
    }
    
    # Sort by importance (descending)
    signal_breakdown = dict(sorted(signal_breakdown.items(), key=lambda x: x[1], reverse=True))
    
    return {
        "score": score,
        "verdict": verdict,
        "signal_breakdown": signal_breakdown
    }


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "SentryPay Fraud Detection API",
        "version": "1.0.0",
        "endpoints": {
            "POST /score": "Score transaction fraud risk",
            "POST /score-recipient": "Score recipient mule account risk",
            "GET /health": "Health check"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
