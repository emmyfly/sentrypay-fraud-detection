"""
Train fraud detection model on synthetic transaction data.
"""
import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, precision_score, recall_score, f1_score
from features import extract_features

def main():
    print("Loading transaction dataset...")
    df = pd.read_csv('../data/transactions.csv')
    
    print(f"Loaded {len(df)} transactions")
    print(f"Fraud rate: {df['label'].mean()*100:.2f}%\n")
    
    # Extract features for all transactions
    print("Extracting features...")
    feature_dicts = []
    for _, row in df.iterrows():
        features = extract_features(row.to_dict())
        feature_dicts.append(features)
    
    # Convert to DataFrame
    X = pd.DataFrame(feature_dicts)
    y = df['label']
    
    print(f"Features extracted: {list(X.columns)}\n")
    
    # Split into train/test (80/20), stratified to preserve fraud rate
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Training set: {len(X_train)} transactions ({y_train.mean()*100:.2f}% fraud)")
    print(f"Test set: {len(X_test)} transactions ({y_test.mean()*100:.2f}% fraud)\n")
    
    # Train Random Forest
    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=20,
        min_samples_leaf=10,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    print("Training complete!\n")
    
    # Evaluate on test set
    print("=" * 60)
    print("EVALUATION ON TEST SET")
    print("=" * 60)
    
    y_pred = model.predict(X_test)
    
    # Detailed metrics
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    print(f"\nPrecision: {precision:.3f} (of flagged transactions, {precision*100:.1f}% are actually fraud)")
    print(f"Recall: {recall:.3f} (catches {recall*100:.1f}% of all fraud cases)")
    print(f"F1-Score: {f1:.3f}\n")
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    print("Confusion Matrix:")
    print("                  Predicted Normal  Predicted Fraud")
    print(f"Actually Normal        {cm[0][0]:6d}           {cm[0][1]:6d}")
    print(f"Actually Fraud         {cm[1][0]:6d}           {cm[1][1]:6d}")
    
    false_negatives = cm[1][0]
    false_positives = cm[0][1]
    true_positives = cm[1][1]
    true_negatives = cm[0][0]
    
    print(f"\n✗ False Negatives: {false_negatives} (missed fraud cases - very bad!)")
    print(f"✗ False Positives: {false_positives} (wrongly flagged normal transactions)")
    print(f"✓ True Positives: {true_positives} (correctly caught fraud)")
    print(f"✓ True Negatives: {true_negatives} (correctly identified normal)\n")
    
    # Classification report
    print("\nDetailed Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['Normal', 'Fraud']))
    
    # Feature importance
    print("\n" + "=" * 60)
    print("FEATURE IMPORTANCE")
    print("=" * 60)
    
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nTop features for detecting fraud:")
    for idx, row in feature_importance.iterrows():
        print(f"  {row['feature']:30s} {row['importance']:.4f}")
    
    # Save model
    print("\n" + "=" * 60)
    model_path = 'model.pkl'
    with open(model_path, 'wb') as f:
        pickle.dump({
            'model': model,
            'feature_names': list(X.columns)
        }, f)
    
    print(f"✓ Model saved to {model_path}")
    print("=" * 60)

if __name__ == "__main__":
    main()
