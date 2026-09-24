"""
Train mule account detection model on recipient risk data.
"""
import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, precision_score, recall_score, f1_score
from features import extract_recipient_features

def main():
    print("Loading recipient risk dataset...")
    df = pd.read_csv('../data/recipient_risk.csv')
    
    # Aggregate by recipient to get one row per recipient
    recipient_agg = df.groupby('recipient_id').agg({
        'num_transactions': 'sum',
        'avg_amount': 'mean',
        'days_span': 'min',  # Shortest span (most concentrated)
        'unique_senders_30d': 'first',
        'first_time_senders_30d': 'first',
        'label': 'first'
    }).reset_index()
    
    print(f"Loaded {len(recipient_agg)} unique recipients")
    print(f"Mule account rate: {recipient_agg['label'].mean()*100:.2f}%\n")
    
    # Extract features for all recipients
    print("Extracting features...")
    feature_dicts = []
    for _, row in recipient_agg.iterrows():
        features = extract_recipient_features(row.to_dict())
        feature_dicts.append(features)
    
    # Convert to DataFrame
    X = pd.DataFrame(feature_dicts)
    y = recipient_agg['label']
    
    print(f"Features extracted: {list(X.columns)}\n")
    
    # Split into train/test (80/20), stratified
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Training set: {len(X_train)} recipients ({y_train.mean()*100:.2f}% mule accounts)")
    print(f"Test set: {len(X_test)} recipients ({y_test.mean()*100:.2f}% mule accounts)\n")
    
    # Train Random Forest
    print("Training Random Forest Classifier for mule detection...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=10,
        min_samples_leaf=5,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    print("Training complete!\n")
    
    # Evaluate on test set
    print("=" * 60)
    print("EVALUATION ON TEST SET - MULE ACCOUNT DETECTION")
    print("=" * 60)
    
    y_pred = model.predict(X_test)
    
    # Detailed metrics
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    print(f"\nPrecision: {precision:.3f} (of flagged recipients, {precision*100:.1f}% are actually mule accounts)")
    print(f"Recall: {recall:.3f} (catches {recall*100:.1f}% of all mule accounts)")
    print(f"F1-Score: {f1:.3f}\n")
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    print("Confusion Matrix:")
    print("                      Predicted Normal  Predicted Mule")
    print(f"Actually Normal           {cm[0][0]:6d}          {cm[0][1]:6d}")
    print(f"Actually Mule Account     {cm[1][0]:6d}          {cm[1][1]:6d}")
    
    false_negatives = cm[1][0]
    false_positives = cm[0][1]
    true_positives = cm[1][1]
    true_negatives = cm[0][0]
    
    print(f"\n✗ False Negatives: {false_negatives} (missed mule accounts)")
    print(f"✗ False Positives: {false_positives} (wrongly flagged normal recipients)")
    print(f"✓ True Positives: {true_positives} (correctly identified mule accounts)")
    print(f"✓ True Negatives: {true_negatives} (correctly identified normal recipients)\n")
    
    # Classification report
    print("\nDetailed Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['Normal Recipient', 'Mule Account']))
    
    # Feature importance
    print("\n" + "=" * 60)
    print("FEATURE IMPORTANCE - MULE DETECTION")
    print("=" * 60)
    
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nTop features for detecting mule accounts:")
    for idx, row in feature_importance.iterrows():
        print(f"  {row['feature']:30s} {row['importance']:.4f}")
    
    # Save model
    print("\n" + "=" * 60)
    model_path = 'mule_model.pkl'
    with open(model_path, 'wb') as f:
        pickle.dump({
            'model': model,
            'feature_names': list(X.columns)
        }, f)
    
    print(f"✓ Mule detection model saved to {model_path}")
    print("=" * 60)

if __name__ == "__main__":
    main()
