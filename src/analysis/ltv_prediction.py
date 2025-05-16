import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import os
from pathlib import Path

def calculate_ltv():
    project_root = Path(__file__).parent.parent.parent
    clusters_path = project_root / 'data' / 'processed' / 'clusters.csv'
    
    clusters = pd.read_csv(clusters_path)

    clusters['predicted_ltv'] = (clusters['monetary'] * clusters['frequency'] * 12)\
          / (1 + clusters['recency']/30)
    
    output_path = project_root / 'data' / 'processed' / 'clusters_with_ltv.csv'
    clusters.to_csv(output_path, index=False)
    
    print(f"LTV прогноз сохранен в: {output_path}")
    return clusters

if __name__ == '__main__':
    calculate_ltv()

