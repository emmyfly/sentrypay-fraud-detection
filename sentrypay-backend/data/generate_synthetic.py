import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_normal_transactions(n=5000):
    """Generate normal banking transactions."""
    transactions = []
    
    # Create pools of IDs for realistic patterns
    account_ids = [f"ACC{str(i).zfill(6)}" for i in range(1, 1001)]
    device_ids = [f"DEV{str(i).zfill(6)}" for i in range(1, 1201)]
    sim_ids = [f"SIM{str(i).zfill(6)}" for i in range(1, 1201)]
    recipient_ids = [f"RCP{str(i).zfill(6)}" for i in range(1, 801)]
    
    # Track recipient history for each account
    account_recipients = {}
    
    for _ in range(n):
        account_id = random.choice(account_ids)
        
        # Initialize recipient history for new accounts
        if account_id not in account_recipients:
            account_recipients[account_id] = {}
        
        # 80% chance of sending to known recipient
        is_known = random.random() < 0.8 and len(account_recipients[account_id]) > 0
        
        if is_known:
            recipient_id = random.choice(list(account_recipients[account_id].keys()))
            account_recipients[account_id][recipient_id] += 1
        else:
            recipient_id = random.choice(recipient_ids)
            if recipient_id not in account_recipients[account_id]:
                account_recipients[account_id][recipient_id] = 0
            account_recipients[account_id][recipient_id] += 1
        
        recipient_transfer_count = account_recipients[account_id][recipient_id]
        
        # Normal amounts: mostly ₦500 - ₦50,000
        amount = np.random.lognormal(9.5, 1.2)  # Log-normal distribution
        amount = max(500, min(50000, amount))
        amount = round(amount, 2)
        
        # Normal waking hours (6 AM - 11 PM weighted)
        hour_of_day = int(np.random.normal(14, 4))  # Peak around 2 PM
        hour_of_day = max(6, min(23, hour_of_day))
        
        # Devices/SIMs haven't changed recently (high days since change)
        days_since_device_change = int(np.random.exponential(120)) + 30
        days_since_sim_change = int(np.random.exponential(150)) + 30
        
        device_id = random.choice(device_ids)
        sim_id = random.choice(sim_ids)
        
        transactions.append({
            'account_id': account_id,
            'device_id': device_id,
            'sim_id': sim_id,
            'recipient_id': recipient_id,
            'amount': amount,
            'hour_of_day': hour_of_day,
            'is_known_recipient': is_known,
            'days_since_device_change': days_since_device_change,
            'days_since_sim_change': days_since_sim_change,
            'recipient_transfer_count': recipient_transfer_count,
            'label': 0
        })
    
    return pd.DataFrame(transactions)

def generate_fraud_transactions(n=500):
    """Generate fraudulent transactions (SIM-swap pattern)."""
    transactions = []
    
    account_ids = [f"ACC{str(i).zfill(6)}" for i in range(1, 1001)]
    device_ids = [f"DEV{str(i).zfill(6)}" for i in range(1, 1201)]
    sim_ids = [f"SIM{str(i).zfill(6)}" for i in range(1, 1201)]
    recipient_ids = [f"RCP{str(i).zfill(6)}" for i in range(1, 801)]
    
    for _ in range(n):
        account_id = random.choice(account_ids)
        device_id = random.choice(device_ids)
        sim_id = random.choice(sim_ids)
        
        # Unknown recipient (fraudster's account)
        recipient_id = random.choice(recipient_ids)
        
        # Large amounts: ₦80,000 - ₦500,000
        amount = np.random.uniform(80000, 500000)
        amount = round(amount, 2)
        
        # Unusual hours weighted toward late night/early morning
        hour_distribution = [0, 0, 1, 1, 2, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 
                           13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 23]
        hour_of_day = random.choice(hour_distribution)
        
        # Recent device/SIM change (SIM-swap indicator)
        days_since_device_change = int(np.random.exponential(2))  # Very recent
        days_since_sim_change = int(np.random.exponential(2))  # Very recent
        
        transactions.append({
            'account_id': account_id,
            'device_id': device_id,
            'sim_id': sim_id,
            'recipient_id': recipient_id,
            'amount': amount,
            'hour_of_day': hour_of_day,
            'is_known_recipient': False,
            'days_since_device_change': days_since_device_change,
            'days_since_sim_change': days_since_sim_change,
            'recipient_transfer_count': 0,
            'label': 1
        })
    
    return pd.DataFrame(transactions)

def generate_recipient_risk_dataset():
    """Generate recipient-side risk dataset (mule account detection)."""
    recipient_ids = [f"RCP{str(i).zfill(6)}" for i in range(1, 301)]
    sender_ids = [f"ACC{str(i).zfill(6)}" for i in range(1, 1501)]
    
    recipients = []
    
    # Normal recipients: steady, familiar senders
    for i in range(200):
        recipient_id = recipient_ids[i]
        
        # Each normal recipient has 3-8 regular senders
        num_senders = random.randint(3, 8)
        regular_senders = random.sample(sender_ids, num_senders)
        
        # Generate transactions over time
        for sender in regular_senders:
            # Multiple transactions from same sender over weeks/months
            num_transactions = random.randint(5, 30)
            
            recipients.append({
                'recipient_id': recipient_id,
                'sender_id': sender,
                'num_transactions': num_transactions,
                'avg_amount': round(np.random.uniform(2000, 25000), 2),
                'days_span': random.randint(30, 365),  # Transactions spread over time
                'unique_senders_30d': num_senders,
                'first_time_senders_30d': 0,
                'label': 0  # Normal
            })
    
    # Mule accounts: many first-time senders in short window
    for i in range(200, 250):
        recipient_id = recipient_ids[i]
        
        # Mule account receives from many different senders
        num_senders = random.randint(15, 50)
        different_senders = random.sample(sender_ids, num_senders)
        
        for sender in different_senders:
            # Typically just 1-2 transactions per sender (quick cash-out)
            num_transactions = random.randint(1, 2)
            
            recipients.append({
                'recipient_id': recipient_id,
                'sender_id': sender,
                'num_transactions': num_transactions,
                'avg_amount': round(np.random.uniform(50000, 400000), 2),
                'days_span': random.randint(1, 7),  # All within a week
                'unique_senders_30d': num_senders,
                'first_time_senders_30d': num_senders,  # All are first-time
                'label': 1  # Mule account
            })
    
    return pd.DataFrame(recipients)

def main():
    print("Generating synthetic fraud detection datasets...\n")
    
    # Generate transaction dataset
    print("Generating normal transactions...")
    normal_df = generate_normal_transactions(5000)
    
    print("Generating fraudulent transactions...")
    fraud_df = generate_fraud_transactions(500)
    
    # Combine and shuffle
    transactions_df = pd.concat([normal_df, fraud_df], ignore_index=True)
    transactions_df = transactions_df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Save transaction dataset
    transactions_df.to_csv('data/transactions.csv', index=False)
    
    print(f"\n=== Transaction Dataset Stats ===")
    print(f"Total transactions: {len(transactions_df)}")
    print(f"Normal transactions: {len(normal_df)} ({len(normal_df)/len(transactions_df)*100:.1f}%)")
    print(f"Fraudulent transactions: {len(fraud_df)} ({len(fraud_df)/len(transactions_df)*100:.1f}%)")
    print(f"Fraud rate: {transactions_df['label'].mean()*100:.2f}%")
    print(f"\nAmount statistics:")
    print(f"  Normal - Mean: ₦{normal_df['amount'].mean():,.2f}, Median: ₦{normal_df['amount'].median():,.2f}")
    print(f"  Fraud - Mean: ₦{fraud_df['amount'].mean():,.2f}, Median: ₦{fraud_df['amount'].median():,.2f}")
    print(f"\nDevice/SIM change statistics:")
    print(f"  Normal - Avg days since device change: {normal_df['days_since_device_change'].mean():.1f}")
    print(f"  Fraud - Avg days since device change: {fraud_df['days_since_device_change'].mean():.1f}")
    print(f"  Normal - Avg days since SIM change: {normal_df['days_since_sim_change'].mean():.1f}")
    print(f"  Fraud - Avg days since SIM change: {fraud_df['days_since_sim_change'].mean():.1f}")
    
    # Generate recipient risk dataset
    print("\n\nGenerating recipient risk dataset...")
    recipients_df = generate_recipient_risk_dataset()
    recipients_df.to_csv('data/recipient_risk.csv', index=False)
    
    print(f"\n=== Recipient Risk Dataset Stats ===")
    print(f"Total recipient records: {len(recipients_df)}")
    print(f"Normal recipients: {recipients_df[recipients_df['label']==0]['recipient_id'].nunique()}")
    print(f"Mule accounts: {recipients_df[recipients_df['label']==1]['recipient_id'].nunique()}")
    
    normal_recipients = recipients_df[recipients_df['label']==0]
    mule_recipients = recipients_df[recipients_df['label']==1]
    
    print(f"\nNormal recipient pattern:")
    print(f"  Avg unique senders (30d): {normal_recipients['unique_senders_30d'].mean():.1f}")
    print(f"  Avg first-time senders (30d): {normal_recipients['first_time_senders_30d'].mean():.1f}")
    
    print(f"\nMule account pattern:")
    print(f"  Avg unique senders (30d): {mule_recipients['unique_senders_30d'].mean():.1f}")
    print(f"  Avg first-time senders (30d): {mule_recipients['first_time_senders_30d'].mean():.1f}")
    
    print(f"\n✓ Datasets saved to data/transactions.csv and data/recipient_risk.csv")

if __name__ == "__main__":
    main()
