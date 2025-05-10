import pandas as pd
from datetime import datetime
import os

def calculate_rfm():
    df = pd.read_csv('data/raw/client_data.csv', parse_dates=['purchase_date', 'last_visit_date'])
    
    snapshot_date = df['purchase_date'].max() + pd.Timedelta(days=1)
    
    rfm = df.groupby('client_id').agg({
        'purchase_date': lambda x: (snapshot_date - x.max()).days,
        'transaction_id': 'count',
        'purchase_amount': 'sum'
    }).reset_index()
    
    rfm.columns = ['client_id', 'recency', 'frequency', 'monetary']
    
    os.makedirs('data/processed', exist_ok=True)
    rfm.to_csv('data/processed/rfm_data.csv', index=False)
    
    return rfm

if __name__ == '__main__':
    calculate_rfm()