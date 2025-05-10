import os
from pathlib import Path

class Config:
    # Базовые пути
    BASE_DIR = Path(__file__).parent.parent  # Корень проекта
    
    # Пути к данным
    RAW_DATA = BASE_DIR / 'data/raw/client_data.csv'
    PROCESSED_DATA = BASE_DIR / 'data/processed/rfm_data.csv'
    CLUSTERED_DATA = BASE_DIR / 'data/processed/clustered_data.csv'
    
    # Пути к результатам
    PLOTS_DIR = BASE_DIR / 'results/plots'
    REPORTS_DIR = BASE_DIR / 'results/reports'
    
    # Создание директорий при необходимости
    for path in [PLOTS_DIR, REPORTS_DIR]:
        path.mkdir(parents=True, exist_ok=True)