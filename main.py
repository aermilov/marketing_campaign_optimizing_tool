from src.analysis.rfm_analysis import calculate_rfm_metrics
from src.analysis.clustering import perform_clustering
from src.analysis.ltv_prediction import calculate_ltv
from src.analysis.churn_analysis import analyze_churn


if __name__ == "__main__":
    calculate_rfm_metrics()
    perform_clustering()
    calculate_ltv()
    analyze_churn()