import pandas as pd
import os
from datetime import datetime

def calculate_platform_roi():
    clients = pd.read_csv('data/raw/client_data.csv', parse_dates=['purchase_date'])
    marketing = pd.read_csv('data/raw/marketing_spend.csv', parse_dates=['date'])
    
    platform_revenue = clients.groupby('traffic_source')['purchase_amount']\
        .agg(['sum', 'count'])\
        .rename(columns={'sum': 'revenue', 'count': 'purchases'})\
        .reset_index()
    
    platform_stats = marketing.groupby('platform').agg({
        'spend': 'sum',
        'impressions': 'sum',
        'clicks': 'sum'
    }).reset_index()
    
    merged = pd.merge(
        platform_revenue, 
        platform_stats, 
        left_on='traffic_source', 
        right_on='platform',
        how='left'
    ).fillna(0)
    
    merged['roi'] = (merged['revenue'] - merged['spend']) / merged['spend']
    merged['cpc'] = merged['spend'] / merged['clicks']
    merged['conversion_rate'] = merged['purchases'] / merged['clicks']
    
    os.makedirs('data/processed', exist_ok=True)
    merged.to_csv('data/processed/platform_roi.csv', index=False)
    
    return merged

if __name__ == '__main__':
    roi_data = calculate_platform_roi()
    print("Результаты анализа ROI:")
    print(roi_data[['platform', 'spend', 'revenue', 'roi', 'cpc', 'conversion_rate']].to_string())