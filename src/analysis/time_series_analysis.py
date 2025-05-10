import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path
import warnings
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_percentage_error

# Настройки для стабильности
warnings.filterwarnings("ignore")
plt.style.use('ggplot')
pd.options.mode.chained_assignment = None

def load_and_prepare_data():
    """Загрузка и подготовка данных"""
    project_root = Path(__file__).parent.parent.parent
    try:
        client_data = pd.read_csv(
            project_root / 'data/raw/client_data.csv',
            parse_dates=['purchase_date']
        )
        
        # Агрегация по месяцам
        monthly_profit = client_data.groupby(
            pd.Grouper(key='purchase_date', freq='ME')
        )['purchase_amount'].sum().to_frame('profit')
        
        # Заполнение пропусков простой интерполяцией
        if monthly_profit['profit'].isnull().sum() > 0:
            monthly_profit['profit'] = monthly_profit['profit'].interpolate()
            
        return monthly_profit.dropna()
    
    except Exception as e:
        print(f"Ошибка загрузки данных: {str(e)}")
        return None

def exponential_smoothing_forecast(data, periods=12):
    """Прогноз с помощью тройного экспоненциального сглаживания"""
    try:
        model = ExponentialSmoothing(
            data['profit'],
            trend='add',
            seasonal='add',
            seasonal_periods=12
        ).fit()
        return model.forecast(periods)
    except:
        # Если не хватает данных для сезонной модели, используем простую
        try:
            model = ExponentialSmoothing(
                data['profit'],
                trend='add'
            ).fit()
            return model.forecast(periods)
        except Exception as e:
            print(f"Ошибка Exp Smoothing: {str(e)}")
            return None

def random_forest_forecast(data, periods=12):
    """Прогноз с помощью Random Forest"""
    try:
        # Создаем признаки
        df = data.copy()
        df['month'] = df.index.month
        df['year'] = df.index.year
        for lag in [1, 2, 3, 12]:  # Лаги 1,2,3 месяца и годовой
            df[f'lag_{lag}'] = df['profit'].shift(lag)
        df = df.dropna()
        
        if len(df) < 10:  # Минимум 10 наблюдений
            raise ValueError("Недостаточно данных для RF")
            
        X = df.drop('profit', axis=1)
        y = df['profit']
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        model = RandomForestRegressor(
            n_estimators=100,
            random_state=42,
            max_depth=5
        )
        model.fit(X_scaled, y)
        
        last_data = df.iloc[-1]
        forecasts = []
        
        for i in range(periods):
            next_month = (last_data['month'] + i) % 12 or 12
            next_year = last_data['year'] + (last_data['month'] + i - 1) // 12
            
            features = [next_month, next_year]
            for lag in [1, 2, 3, 12]:
                if lag == 1 and forecasts:
                    features.append(forecasts[-1])
                elif len(forecasts) >= lag:
                    features.append(forecasts[-lag])
                else:
                    features.append(df['profit'].iloc[-lag + len(forecasts)])
            
            X_new = scaler.transform([features])
            pred = model.predict(X_new)[0]
            forecasts.append(pred)
            
        return np.array(forecasts)
    except Exception as e:
        print(f"Ошибка Random Forest: {str(e)}")
        return None

def plot_and_save_results(data, es_forecast, rf_forecast, periods=12):
    """Визуализация и сохранение результатов"""
    project_root = Path(__file__).parent.parent.parent
    
    # Подготовка дат прогноза
    forecast_index = pd.date_range(
        start=data.index[-1] + pd.DateOffset(months=1),
        periods=periods,
        freq='ME'
    )
    
    # Создание графика
    plt.figure(figsize=(15, 7))
    plt.plot(data.index, data['profit'], label='Фактические данные', color='blue', linewidth=2)
    
    if es_forecast is not None:
        plt.plot(forecast_index, es_forecast, 
                label='Прогноз (Exp Smoothing)', 
                color='red', linestyle='--', linewidth=2)
    
    if rf_forecast is not None:
        plt.plot(forecast_index, rf_forecast,
                label='Прогноз (Random Forest)',
                color='green', linestyle=':', linewidth=2)
    
    plt.title('Прогноз прибыли на 12 месяцев', fontsize=16, pad=20)
    plt.xlabel('Дата', fontsize=12)
    plt.ylabel('Прибыль, руб.', fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # Сохранение графика
    os.makedirs(project_root / 'results/plots', exist_ok=True)
    plt.savefig(project_root / 'results/plots/profit_forecast.png', 
               bbox_inches='tight', dpi=300)
    plt.close()
    
    # Сохранение данных
    forecast_df = pd.DataFrame({
        'date': forecast_index,
        'exp_smoothing_forecast': es_forecast if es_forecast is not None else [np.nan]*periods,
        'random_forest_forecast': rf_forecast if rf_forecast is not None else [np.nan]*periods
    })
    
    os.makedirs(project_root / 'data/processed', exist_ok=True)
    forecast_df.to_csv(project_root / 'data/processed/profit_forecast.csv', index=False)
    
    return forecast_df

def analyze_profit_trend():
    """Основная функция анализа"""
    try:
        monthly_profit = load_and_prepare_data()
        if monthly_profit is None:
            return None
            
        if len(monthly_profit) < 6:
            print("Недостаточно данных для анализа (минимум 6 месяцев)")
            return None
        
        es_forecast = exponential_smoothing_forecast(monthly_profit)
        rf_forecast = random_forest_forecast(monthly_profit)
        
        result = plot_and_save_results(monthly_profit, es_forecast, rf_forecast)
        
        print("Прогноз успешно сгенерирован!")
        return result
        
    except Exception as e:
        print(f"Ошибка в основном анализе: {str(e)}")
        return None

if __name__ == '__main__':
    print("Запуск анализа прибыли...")
    result = analyze_profit_trend()
    if result is not None:
        print("\nПервые строки прогноза:")
        print(result.head())

