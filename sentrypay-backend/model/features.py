"""
Feature extraction for fraud detection.
This module is designed to work on single transactions (dicts) so it can be reused
in the live API without pandas dependencies.
"""

def extract_features(row):
    """
    Extract features from a single transaction for fraud detection.
    
    Args:
        row: dict with keys: amount, hour_of_day, is_known_recipient,
             days_since_device_change, days_since_sim_change, recipient_transfer_count
    
    Returns:
        dict of features ready for model input
    """
    features = {}
    
    # Amount-based features
    features['amount'] = float(row['amount'])
    features['amount_log'] = float(row['amount']) if row['amount'] > 0 else 0
    if features['amount_log'] > 0:
        import math
        features['amount_log'] = math.log(features['amount_log'])
    
    # Amount buckets (high-value transfers are riskier)
    features['is_high_value'] = 1 if row['amount'] > 100000 else 0
    features['is_very_high_value'] = 1 if row['amount'] > 300000 else 0
    
    # Time-based features
    features['hour_of_day'] = int(row['hour_of_day'])
    features['is_night_time'] = 1 if row['hour_of_day'] < 6 or row['hour_of_day'] > 22 else 0
    features['is_unusual_hour'] = 1 if row['hour_of_day'] < 6 or row['hour_of_day'] > 23 else 0
    
    # Recipient familiarity
    features['is_known_recipient'] = 1 if row['is_known_recipient'] else 0
    features['recipient_transfer_count'] = int(row['recipient_transfer_count'])
    features['is_first_time_recipient'] = 1 if row['recipient_transfer_count'] == 0 else 0
    
    # Device/SIM change indicators (key for SIM-swap detection)
    features['days_since_device_change'] = int(row['days_since_device_change'])
    features['days_since_sim_change'] = int(row['days_since_sim_change'])
    
    # Risk flags: recent device/SIM changes
    features['recent_device_change'] = 1 if row['days_since_device_change'] < 7 else 0
    features['recent_sim_change'] = 1 if row['days_since_sim_change'] < 7 else 0
    features['very_recent_device_change'] = 1 if row['days_since_device_change'] < 3 else 0
    features['very_recent_sim_change'] = 1 if row['days_since_sim_change'] < 3 else 0
    
    # Combined risk indicators
    features['device_and_sim_changed'] = 1 if (row['days_since_device_change'] < 7 and 
                                                 row['days_since_sim_change'] < 7) else 0
    
    # High-risk pattern: new recipient + recent device/SIM change + high value
    features['high_risk_pattern'] = 1 if (row['recipient_transfer_count'] == 0 and
                                          row['days_since_device_change'] < 7 and
                                          row['amount'] > 50000) else 0
    
    return features


def extract_recipient_features(row):
    """
    Extract features for recipient-side risk (mule account detection).
    
    Args:
        row: dict with keys from recipient_risk dataset
    
    Returns:
        dict of features for mule account detection
    """
    features = {}
    
    # Transaction patterns
    features['num_transactions'] = int(row['num_transactions'])
    features['avg_amount'] = float(row['avg_amount'])
    features['days_span'] = int(row['days_span'])
    
    # Sender diversity (key mule indicator)
    features['unique_senders_30d'] = int(row['unique_senders_30d'])
    features['first_time_senders_30d'] = int(row['first_time_senders_30d'])
    
    # Derived features
    features['first_time_sender_ratio'] = (float(row['first_time_senders_30d']) / 
                                           row['unique_senders_30d'] if row['unique_senders_30d'] > 0 else 0)
    
    # High-value + many first-time senders = mule pattern
    features['high_value_many_senders'] = 1 if (row['avg_amount'] > 100000 and 
                                                 row['unique_senders_30d'] > 10) else 0
    
    # Velocity indicators
    features['avg_transactions_per_sender'] = (float(row['num_transactions']) / 
                                               row['unique_senders_30d'] if row['unique_senders_30d'] > 0 else 0)
    
    features['transactions_per_day'] = (float(row['num_transactions']) / 
                                       row['days_span'] if row['days_span'] > 0 else 0)
    
    # Mule red flags
    features['many_unique_senders'] = 1 if row['unique_senders_30d'] > 15 else 0
    features['mostly_first_time'] = 1 if features['first_time_sender_ratio'] > 0.8 else 0
    features['concentrated_timeframe'] = 1 if row['days_span'] < 7 else 0
    
    return features
