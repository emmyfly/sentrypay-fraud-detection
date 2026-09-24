# How SentryPay's Fraud Detection Works

A complete technical explanation of the ML-powered fraud detection system.

---

## 🎯 The Big Picture

**Goal**: Detect fraudulent bank transactions in real-time, especially SIM-swap attacks where criminals take over a victim's phone number to steal money.

**Method**: Machine Learning (RandomForest) trained on transaction patterns to predict fraud probability.

---

## 📊 The Complete Flow

```
Transaction → Feature Engineering → ML Model → Risk Score → Action
   (Raw)         (18 features)      (Random     (0-100)    (Safe/Watch/Block)
                                     Forest)
```

---

## 1️⃣ Raw Transaction Data (Input)

When a transaction happens, the system receives 10 raw data points:

```json
{
  "account_id": "ACC000123",           // Sender account
  "device_id": "DEV000456",            // Phone/device used
  "sim_id": "SIM000789",               // SIM card in device
  "recipient_id": "RCP000321",         // Who's receiving money
  "amount": 150000,                    // ₦150,000
  "hour_of_day": 2,                    // 2 AM (suspicious!)
  "is_known_recipient": false,         // First time sending here
  "days_since_device_change": 1,       // Device changed yesterday (!!)
  "days_since_sim_change": 0,          // SIM changed TODAY (!!!)
  "recipient_transfer_count": 0        // Never sent to this person before
}
```

**This looks suspicious because:**
- Large amount (₦150k)
- Late at night (2 AM)
- Unknown recipient
- Device AND SIM just changed (classic SIM-swap attack pattern)

---

## 2️⃣ Feature Engineering (The Secret Sauce)

The model doesn't see raw data. It sees **18 engineered features** that capture fraud patterns:

### A. Amount Features (4 features)
```python
amount = 150000
amount_log = log(150000) = 11.9  # Log scale for better distribution
is_high_value = 1                 # > ₦100k
is_very_high_value = 0            # < ₦300k
```

**Why?** Fraudsters steal large amounts. Log transformation helps the model handle wide ranges.

### B. Time Features (3 features)
```python
hour_of_day = 2
is_night_time = 1        # 2 AM is < 6 or > 22
is_unusual_hour = 1      # 2 AM is < 6 or > 23
```

**Why?** Fraudsters often work at night when victims are asleep.

### C. Recipient Familiarity (3 features)
```python
is_known_recipient = 0           # Never sent here before
recipient_transfer_count = 0     # Zero history
is_first_time_recipient = 1      # First time flag
```

**Why?** Legitimate users send money to people they know. Fraudsters drain to new accounts.

### D. Device/SIM Change Indicators (6 features) ⚠️ CRITICAL
```python
days_since_device_change = 1
days_since_sim_change = 0
recent_device_change = 1         # Changed within 7 days
recent_sim_change = 1            # Changed within 7 days
very_recent_device_change = 0    # Changed within 3 days
very_recent_sim_change = 1       # Changed TODAY
```

**Why?** This is the KEY signal for SIM-swap fraud:
1. Criminal ports victim's phone number to their SIM
2. Gets 2FA codes
3. Logs into banking app
4. Transfers money immediately

A recent SIM/device change + large transfer = huge red flag 🚨

### E. Combined Risk Pattern (2 features)
```python
device_and_sim_changed = 1       # Both changed recently
high_risk_pattern = 1            # First-time recipient + recent device change + > ₦50k
```

**Why?** Combines multiple signals into clear fraud patterns.

---

## 3️⃣ The Machine Learning Model

### What is RandomForest?

Think of it as **100 decision trees voting together**:

```
                    RandomForest
                   /     |      \
               Tree1   Tree2  ... Tree100
                 |       |           |
              Fraud?  Safe?      Fraud?
                 ↓       ↓           ↓
            VOTE: 85 say FRAUD, 15 say SAFE
                 ↓
         Probability = 85/100 = 0.85 (85% fraud)
```

### Each Tree Asks Questions

Example decision tree logic:
```
Is days_since_sim_change < 7?
├─ YES → Is amount > ₦50,000?
│        ├─ YES → Is recipient_transfer_count = 0?
│        │        ├─ YES → 🚨 FRAUD (90% confidence)
│        │        └─ NO → Check more signals...
│        └─ NO → Probably safe
└─ NO → Check other patterns...
```

### Training Process

1. **Learn from 5,500 examples**:
   - 5,000 normal transactions
   - 500 fraudulent transactions

2. **Find patterns**:
   - "When SIM changed recently + large amount + unknown recipient → usually fraud"
   - "When small amount + known recipient + old device → usually safe"

3. **Build 100 trees**, each looking at different feature combinations

4. **Test on 1,100 unseen transactions** → Got 100% accuracy!

---

## 4️⃣ Making Predictions

### Step-by-Step for Our Example

```python
# 1. Extract 18 features from raw transaction
features = extract_features(transaction)
# Result: [150000, 11.9, 1, 0, 2, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1]

# 2. Feed to RandomForest
probability = model.predict_proba(features)
# Result: [0.01, 0.99]  → 1% safe, 99% fraud

# 3. Convert to 0-100 score
score = int(0.99 * 100) = 99

# 4. Apply business rules
if score >= 65:
    verdict = "block"      # ← We land here
elif score >= 35:
    verdict = "watch"
else:
    verdict = "safe"
```

---

## 5️⃣ Feature Importance (Explainability)

The model tells us **which signals mattered most**:

```
Top Features (from training):
1. recipient_transfer_count    19.1%  ← History with recipient
2. amount                      16.2%  ← Transaction size
3. is_first_time_recipient     15.0%  ← New vs known
4. amount_log                  13.1%  ← Log-scaled amount
5. days_since_device_change    13.1%  ← Device change recency ⚠️
6. days_since_sim_change        8.0%  ← SIM change recency ⚠️
7. high_risk_pattern            5.8%  ← Combined red flag
```

**This means:**
- Device/SIM changes are highly predictive (21.1% combined)
- Recipient history is the strongest single signal
- Amount matters, but not as much as behavioral patterns

---

## 🎭 Example Scenarios

### ✅ Safe Transaction (Score: 0)
```json
{
  "amount": 15000,                    // Small amount
  "hour_of_day": 14,                  // 2 PM (normal)
  "is_known_recipient": true,         // Known person
  "days_since_device_change": 120,    // Device stable for months
  "days_since_sim_change": 180,       // SIM stable for months
  "recipient_transfer_count": 5       // Sent here 5 times before
}
```
**Model thinks:** "Normal pattern, regular recipient, stable device → 0% fraud"

### 🚨 Fraudulent Transaction (Score: 100)
```json
{
  "amount": 450000,                   // Large amount!
  "hour_of_day": 3,                   // 3 AM!
  "is_known_recipient": false,        // Unknown recipient!
  "days_since_device_change": 2,      // Device just changed!
  "days_since_sim_change": 1,         // SIM JUST changed!
  "recipient_transfer_count": 0       // First time!
}
```
**Model thinks:** "Classic SIM-swap: new SIM + new device + large transfer to unknown account at 3 AM → 100% fraud"

### 👁️ Suspicious Transaction (Score: 42 - "Watch")
```json
{
  "amount": 75000,                    // Moderate amount
  "hour_of_day": 16,                  // 4 PM (normal)
  "is_known_recipient": false,        // New recipient
  "days_since_device_change": 15,     // Device changed 2 weeks ago
  "days_since_sim_change": 180,       // SIM stable
  "recipient_transfer_count": 0       // First time
}
```
**Model thinks:** "Some red flags (new recipient, recent device change) but not all fraud patterns → flag for review"

---

## 🔄 The Complete System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE                           │
│                 (sentrypay-demo.html)                       │
│                                                             │
│  [Simulate Transaction] → Generates transaction data        │
└──────────────────┬──────────────────────────────────────────┘
                   │ HTTP POST
                   ↓
┌─────────────────────────────────────────────────────────────┐
│                    FASTAPI BACKEND                          │
│                  (api/main.py)                              │
│                                                             │
│  1. Receives JSON transaction                               │
│  2. Calls extract_features()  ────→  [features.py]         │
│  3. Loads trained model       ────→  [model.pkl]           │
│  4. Gets prediction                                         │
│  5. Returns score + verdict + feature importances           │
└──────────────────┬──────────────────────────────────────────┘
                   │ JSON Response
                   ↓
┌─────────────────────────────────────────────────────────────┐
│                    RESPONSE                                 │
│                                                             │
│  {                                                          │
│    "score": 99,                                             │
│    "verdict": "block",                                      │
│    "signal_breakdown": {                                    │
│      "days_since_sim_change": 0.080,                        │
│      "amount": 0.162,                                       │
│      ...                                                    │
│    }                                                        │
│  }                                                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧪 Training vs Production

### Training Phase (Already Done)
```python
# 1. Generate synthetic data
5,500 transactions (90.9% normal, 9.1% fraud)

# 2. Feature engineering
Transform each transaction → 18 features

# 3. Train model
RandomForest learns patterns from 4,400 transactions

# 4. Evaluate
Test on 1,100 unseen transactions → 100% accuracy

# 5. Save model
pickle.dump(model) → model.pkl (59KB)
```

### Production Phase (Live Demo)
```python
# 1. Load trained model once at startup
model = pickle.load('model.pkl')

# 2. For each new transaction:
features = extract_features(transaction)  # Same function used in training
prediction = model.predict_proba(features)
score = int(prediction[1] * 100)

# 3. Return result instantly
```

---

## 🎓 Why This Works

### 1. **Feature Engineering Captures Real Fraud Patterns**
   - SIM-swap attacks have distinct signatures
   - Behavioral patterns (recipient history) beat simple rules
   - Combining multiple signals is more powerful than any single check

### 2. **RandomForest is Robust**
   - Handles non-linear patterns (e.g., "danger increases exponentially when multiple flags trigger")
   - Resistant to overfitting (ensemble of 100 trees)
   - Fast predictions (milliseconds)

### 3. **Explainable Results**
   - Feature importances show why a transaction was flagged
   - Can justify decisions to customers and regulators
   - Helps improve the model over time

### 4. **Real-world Applicable**
   - Trained on realistic Nigerian banking patterns (Naira amounts)
   - Handles imbalanced data (9% fraud rate, like real banking)
   - CORS-enabled API ready for web/mobile integration

---

## 🚀 What Makes This Hackathon-Ready

1. **Actually works**: Not a toy demo, real predictions
2. **Explainable**: Shows feature importances, not a black box
3. **Fast**: Predictions in milliseconds
4. **Scalable**: API can handle concurrent requests
5. **Practical**: Solves real Nigerian banking fraud problem (SIM-swap)
6. **Complete**: End-to-end from data generation to live UI

---

## 📈 Model Performance Details

```
Test Set Results (1,100 transactions):
├─ Precision: 100% (no false alarms)
├─ Recall: 100% (catches all fraud)
├─ F1-Score: 1.000 (perfect balance)
└─ Confusion Matrix:
    Actually Normal: 1000 correct, 0 wrong
    Actually Fraud:  100 correct, 0 missed
```

**In plain English:**
- Caught EVERY fraud case (100/100)
- Didn't falsely accuse ANY normal transactions (0/1000)
- Perfect on synthetic data (would need real-world validation)

---

## 🔮 Future Enhancements

1. **More features**: IP location, transaction velocity, merchant category
2. **Deep learning**: LSTM for sequential patterns
3. **Real-time learning**: Update model with confirmed fraud cases
4. **Recipient network analysis**: Graph neural networks for mule detection
5. **Anomaly detection**: Catch novel fraud patterns

---

## Summary

**SentryPay works by:**
1. Taking raw transaction data (10 fields)
2. Engineering smart features (18 signals) that capture fraud patterns
3. Using a trained RandomForest (100 decision trees) to predict probability
4. Converting probability to actionable score (0-100)
5. Applying business rules (safe/watch/block)
6. Showing which signals triggered the decision (explainability)

**The key insight:** Recent SIM/device changes + unusual transfer patterns = fraud. The ML model learned this from examples and can now detect it automatically! 🎯
