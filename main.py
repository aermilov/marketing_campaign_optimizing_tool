import sys
from pathlib import Path


# Добавляем корень проекта в PYTHONPATH
project_root = Path(__file__).parent
sys.path.append(str(project_root))

def main():
    try:
        # 1. Импортируем модули анализа
        from src.analysis.rfm_analysis import calculate_rfm
        from src.analysis.clustering import perform_clustering
        from src.analysis.roi_analysis import calculate_platform_roi
        from src.analysis.campaign_analysis import analyze_campaigns
        from src.analysis.ltv_prediction import calculate_ltv
        from src.analysis.time_series_analysis import analyze_profit_trend

        # 2. Импортируем модули визуализации
        from src.visualization.plot_rfm import plot_rfm_distribution, plot_clusters_3d
        from src.visualization.plot_campaigns import plot_campaign_performance
        from src.visualization.plot_roi import plot_roi_analysis
        from src.visualization.plot_rfm import plot_cluster_distribution
        
        # 3. Импортируем генератор отчётов
        from src.reporting.generate_report import generate_report

        print("Запуск анализа RFM...")
        calculate_rfm()
        
        print("Выполнение кластеризации...")
        perform_clustering()

        calculate_ltv()
        
        print("Анализ ROI платформ...")
        calculate_platform_roi()
        
        print("Анализ маркетинговых кампаний...")
        analyze_campaigns()
        
        print("Генерация визуализаций...")
        plot_cluster_distribution()
        plot_rfm_distribution()
        plot_clusters_3d()
        plot_campaign_performance()
        plot_roi_analysis()

        print("\nАнализ временных рядов и прогнозирование прибыли...")
        profit_forecast = analyze_profit_trend()
        if profit_forecast is not None:
            print("Прогноз прибыли успешно сгенерирован")
        
        print("Формирование итогового отчёта...")
        generate_report()
        
        print("\nВсе этапы выполнены успешно! Отчёт доступен в results/reports/final_report.html")

    except Exception as e:
        print(f"\nОшибка во время выполнения: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()