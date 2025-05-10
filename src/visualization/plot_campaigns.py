import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_campaign_performance():
    stats = pd.read_csv('data/processed/campaign_stats.csv')
    
    plt.figure(figsize=(10, 6))
    stats.plot(x='platform', y=['ctr', 'cpc'], kind='bar', secondary_y='cpc')
    plt.title('Эффективность рекламных платформ')
    
    # Сохранение
    os.makedirs('results/plots', exist_ok=True)
    plt.savefig('results/plots/campaign_roi.png')
    plt.close()

if __name__ == '__main__':
    plot_campaign_performance()