import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import pandas as pd
import os
from datetime import datetime
import base64

# Настройка путей
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

def calculate_simple_ltv(cluster_data):
    """Рассчитывает простую оценку LTV если нет предсказанных значений"""
    return (cluster_data['monetary'] * cluster_data['frequency'] * 12) / (1 + cluster_data['recency']/30)

def load_cluster_descriptions(cluster_stats):
    """Генерирует подробные описания для каждого кластера"""
    descriptions = []
    
    cluster_profiles = {
        0: {
            "name": "Низкоактивные",
            "description": "Клиенты с низкой частотой покупок и небольшими чеками",
            "strategy": "Требуют реактивации через спецпредложения"
        },
        1: {
            "name": "Лояльные",
            "description": "Постоянные клиенты со средним чеком",
            "strategy": "Программы лояльности и кросс-продажи"
        },
        2: {
            "name": "VIP", 
            "description": "Крупные покупатели с высоким средним чеком",
            "strategy": "Персональный менеджер и эксклюзивные предложения"
        },
        3: {
            "name": "Перспективные",
            "description": "Новые активные клиенты",
            "strategy": "Удержание и повышение частоты покупок"
        }
    }
    
    for cluster_id, stats in cluster_stats.iterrows():
        profile = cluster_profiles.get(cluster_id, {})
        
        descriptions.append({
            "id": cluster_id,
            "name": profile.get("name", f"Кластер {cluster_id}"),
            "description": profile.get("description", ""),
            "avg_recency": round(stats['recency'], 1),
            "avg_frequency": round(stats['frequency'], 1),
            "avg_monetary": int(stats['monetary']),
            "avg_ltv": int(stats.get('predicted_ltv', calculate_simple_ltv(stats))),
            "recommendation": profile.get("strategy", ""),
            "size": int(stats['size']),
            "size_percent": round(stats['size'] / stats['size'].sum() * 100, 1)
        })
    
    return sorted(descriptions, key=lambda x: -x['avg_ltv'])

def analyze_platforms(roi_data):
    """Анализирует эффективность рекламных платформ"""
    roi_data = roi_data.round({
        'roi': 2,
        'cpc': 1,
        'conversion_rate': 4
    })
    
    platforms = roi_data.to_dict('records')
    best = max(platforms, key=lambda x: x['roi'])
    worst = min(platforms, key=lambda x: x['roi'])
    
    return {
        "platforms": platforms,
        "best": best,
        "worst": worst,
        "total_spend": int(roi_data['spend'].sum()),
        "total_revenue": int(roi_data['revenue'].sum())
    }

def generate_report():
    try:
        # Пути к данным
        data_dir = project_root / 'data' / 'processed'
        raw_data_dir = project_root / 'data' / 'raw'
        
        # 1. Загрузка данных
        clusters = pd.read_csv(data_dir / 'clusters_with_ltv.csv')
        roi_data = pd.read_csv(data_dir / 'platform_roi.csv')
        
        # 2. Получаем период анализа из исходных данных
        try:
            client_data = pd.read_csv(raw_data_dir / 'client_data.csv', parse_dates=['purchase_date'])
            period_start = client_data['purchase_date'].min().strftime('%Y-%m-%d')
            period_end = client_data['purchase_date'].max().strftime('%Y-%m-%d')
        except Exception as e:
            print(f"Не удалось загрузить даты: {str(e)}")
            period_start = "неизвестно"
            period_end = "неизвестно"
        
        # 3. Анализ кластеров
        cluster_stats = clusters.groupby('cluster').agg({
            'recency': 'mean',
            'frequency': 'mean',
            'monetary': 'mean',
            'predicted_ltv': 'mean',
            'client_id': 'count'
        }).rename(columns={'client_id': 'size'})
        
        cluster_analysis = load_cluster_descriptions(cluster_stats)
        best_cluster = max(cluster_analysis, key=lambda x: x['avg_ltv'])
        worst_cluster = min(cluster_analysis, key=lambda x: x['avg_ltv'])
        
        # 4. Анализ платформ
        platform_analysis = analyze_platforms(roi_data)

        with open(project_root / 'results' / 'plots' / 'platform_roi.png', 'rb') as img_file:
            roi_img_base64 = base64.b64encode(img_file.read()).decode('utf-8')

        with open(project_root / 'results' / 'plots' / 'cluster_distribution.png', 'rb') as img1_file:
            distrib_base64 = base64.b64encode(img1_file.read()).decode('utf-8')

        clusters_3d_path = '../plots/clusters_3d.html'

        with open(project_root / 'results' / 'plots' / 'profit_forecast.png', 'rb') as img_file2:
            profit_forecast_img = base64.b64encode(img_file2.read()).decode('utf-8')


        # 5. Подготовка данных для отчета
        report_data = {
            "date": datetime.now().strftime("%d.%m.%Y %H:%M"),
            "period": {
                "start": period_start,
                "end": period_end
            },
            "clusters": cluster_analysis,
            "best_cluster": best_cluster,
            "worst_cluster": worst_cluster,
            "platforms": platform_analysis,
            "metrics": {
                "avg_ltv": int(clusters['predicted_ltv'].mean()),
                "total_clients": len(clusters),
                "avg_recency": int(clusters['recency'].mean()),
                "avg_frequency": round(clusters['frequency'].mean(), 1)
            },
            "plots": {
                "clusters": clusters_3d_path,
                "roi": roi_img_base64,
                "distribution": distrib_base64,
                "profit_forecast": profit_forecast_img
            },
        }
        
        # 6. Генерация HTML
        template_dir = project_root / 'src' / 'visualization' / 'templates'
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        template = env.get_template("report_template.html")
        
        # 7. Сохранение отчета
        report_path = project_root / 'results' / 'reports' / 'final_report.html'
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(template.render(report_data))
        
        print(f"Отчёт успешно сгенерирован: {report_path}")
        return True
    
    except Exception as e:
        print(f"Ошибка при генерации отчёта: {str(e)}")
        return False

if __name__ == '__main__':
    generate_report()