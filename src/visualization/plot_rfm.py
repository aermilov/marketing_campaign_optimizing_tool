import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import os
from pathlib import Path

# Конфигурация путей (замените Config на прямое указание путей)
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / 'data' / 'processed'
PLOTS_DIR = BASE_DIR / 'results' / 'plots'

def plot_cluster_distribution():
    """Генерирует график распределения клиентов по кластерам"""
    try:
        # Используем clusters.csv вместо clustered_data.csv
        data_path = DATA_DIR / 'clusters.csv'
        data = pd.read_csv(data_path)
        
        if 'cluster' not in data.columns:
            raise ValueError("В файле clusters.csv отсутствует столбец 'cluster'")
        
        # Создаем график распределения
        plt.figure(figsize=(10, 6))
        counts = data['cluster'].value_counts().sort_index()
        
        # Палитра цветов для кластеров
        colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12'][:len(counts)]
        
        counts.plot(
            kind='bar',
            color=colors,
            edgecolor='black'
        )
        
        plt.title('Распределение клиентов по кластерам', pad=20)
        plt.xlabel('Номер кластера')
        plt.ylabel('Количество клиентов')
        plt.xticks(rotation=0)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Добавляем подписи значений
        for i, v in enumerate(counts):
            plt.text(i, v + 5, str(v), ha='center')
        
        # Сохраняем график
        os.makedirs(PLOTS_DIR, exist_ok=True)
        plot_path = PLOTS_DIR / 'cluster_distribution.png'
        plt.savefig(plot_path, bbox_inches='tight', dpi=300)
        plt.close()
        
        print(f"График распределения сохранен в {plot_path}")
        return str(plot_path.relative_to(BASE_DIR))
    
    except Exception as e:
        print(f"Ошибка при создании графика распределения: {str(e)}")
        return None

def plot_rfm_distribution():
    """Генерирует гистограммы RFM-метрик"""
    try:
        rfm_path = DATA_DIR / 'rfm_data.csv'
        rfm = pd.read_csv(rfm_path)
        
        # Создаем гистограммы
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        rfm['recency'].plot(kind='hist', ax=axes[0], title='Recency (Дни с последней покупки)')
        rfm['frequency'].plot(kind='hist', ax=axes[1], title='Frequency (Частота покупок)')
        rfm['monetary'].plot(kind='hist', ax=axes[2], title='Monetary (Сумма покупок)')
        
        # Сохраняем график
        os.makedirs(PLOTS_DIR, exist_ok=True)
        plot_path = PLOTS_DIR / 'rfm_distribution.png'
        plt.savefig(plot_path, bbox_inches='tight')
        plt.close()
        
        print(f"Графики RFM сохранены в {plot_path}")
        return str(plot_path.relative_to(BASE_DIR))
    
    except Exception as e:
        print(f"Ошибка при создании RFM графиков: {str(e)}")
        return None

def plot_clusters_3d():
    """Создает 3D визуализацию кластеров"""
    try:
        clusters_path = DATA_DIR / 'clusters.csv'
        data = pd.read_csv(clusters_path)
        
        fig = px.scatter_3d(
            data,
            x='recency',
            y='frequency',
            z='monetary',
            color='cluster',
            title='3D визуализация RFM-кластеров',
            labels={
                'recency': 'Recency (дни)',
                'frequency': 'Frequency',
                'monetary': 'Monetary (руб)'
            }
        )
        
        # Сохраняем график
        os.makedirs(PLOTS_DIR, exist_ok=True)
        plot_path = PLOTS_DIR / 'clusters_3d.html'
        fig.write_html(plot_path)
        
        print(f"3D визуализация сохранена в {plot_path}")
        return str(plot_path.relative_to(BASE_DIR))
    
    except Exception as e:
        print(f"Ошибка при создании 3D визуализации: {str(e)}")
        return None

if __name__ == '__main__':
    plot_cluster_distribution()
    plot_rfm_distribution()
    plot_clusters_3d()