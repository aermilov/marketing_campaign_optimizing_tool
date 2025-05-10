import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_roi_analysis():
    # Загрузка данных
    roi = pd.read_csv('data/processed/platform_roi.csv')
    
    # Создание графиков
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # График ROI
    roi.sort_values('roi', ascending=False).plot.bar(
        x='platform', y='roi', ax=ax1, title='ROI по платформам'
    )
    ax1.set_ylabel('ROI (доход/расход)')
    
    # График доходов vs расходов
    roi.plot.bar(
        x='platform', 
        y=['spend', 'revenue'], 
        ax=ax2, 
        title='Расходы vs Доходы'
    )
    ax2.set_ylabel('Сумма (руб)')
    
    # Сохранение
    os.makedirs('results/plots', exist_ok=True)
    plt.tight_layout()
    plt.savefig('results/plots/platform_roi.png')
    plt.close()

if __name__ == '__main__':
    plot_roi_analysis()