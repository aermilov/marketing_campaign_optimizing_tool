import pandas as pd
import os

def analyze_campaigns():
    # Загрузка данных
    clients = pd.read_csv('data/raw/client_data.csv')
    spends = pd.read_csv('data/raw/marketing_spend.csv', parse_dates=['date'])
    
    platform_stats = spends.groupby('platform').agg({
        'spend': 'sum',
        'impressions': 'sum',
        'clicks': 'sum'
    }).reset_index()
    
    platform_stats['ctr'] = platform_stats['clicks'] / platform_stats['impressions']
    platform_stats['cpc'] = platform_stats['spend'] / platform_stats['clicks']
    
    os.makedirs('data/processed', exist_ok=True)
    platform_stats.to_csv('data/processed/campaign_stats.csv', index=False)
    
    return platform_stats

if __name__ == '__main__':
    analyze_campaigns()