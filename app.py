import streamlit as st
import pandas as pd
import os
from pathlib import Path
import subprocess
import time
import base64
import traceback

# Настройка страницы
st.set_page_config(
    page_title="Оптимизация маркетинговых кампаний", 
    page_icon="📊",
    layout="wide"
)

# Пути к файлам
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data" / "raw"
RESULTS_DIR = BASE_DIR / "results"
REPORTS_DIR = RESULTS_DIR / "reports"
PLOTS_DIR = RESULTS_DIR / "plots"

# Создаем необходимые директории
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR, exist_ok=True)

st.title("📊 Оптимизация маркетинговых кампаний")
st.markdown("---")

def embed_html_report(report_path):
    """Функция для встраивания HTML-отчета с 3D визуализацией"""
    try:
        # Читаем основной отчет
        with open(report_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # Обрабатываем 3D визуализацию
        clusters_3d_path = PLOTS_DIR / "clusters_3d.html"
        if clusters_3d_path.exists():
            with open(clusters_3d_path, "r", encoding="utf-8") as f:
                clusters_3d_content = f.read()
            
            # Встраиваем содержимое напрямую в отчет
            html_content = html_content.replace(
                '<iframe src="../plots/clusters_3d.html"',
                f'<div class="plot-3d-container">{clusters_3d_content}</div><iframe src="about:blank"'
            )
        
        # Добавляем стили для корректного отображения
        styled_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ margin: 0; padding: 0; font-family: Arial, sans-serif; }}
                .plot-3d-container {{ width: 100%; height: 600px; margin-bottom: 20px; }}
                iframe {{ display: none; }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        return styled_html
    
    except Exception as e:
        st.error(f"Ошибка обработки отчета: {str(e)}")
        st.code(traceback.format_exc())
        return None

# Загрузка данных
with st.expander("🔼 Загрузите данные для анализа", expanded=True):
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Данные клиентов")
        client_file = st.file_uploader(
            "Выберите файл client_data.csv", 
            type="csv",
            key="client_data"
        )
        
    with col2:
        st.subheader("Данные о рекламе")
        marketing_file = st.file_uploader(
            "Выберите файл marketing_spend.csv", 
            type="csv",
            key="marketing_data"
        )

# Кнопка анализа
if client_file and marketing_file:
    if st.button("🚀 Запустить анализ", use_container_width=True):
        with st.spinner("Сохранение данных..."):
            # Сохраняем загруженные файлы
            client_path = DATA_DIR / "client_data.csv"
            marketing_path = DATA_DIR / "marketing_spend.csv"
            
            with open(client_path, "wb") as f:
                f.write(client_file.getbuffer())
            
            with open(marketing_path, "wb") as f:
                f.write(marketing_file.getbuffer())
            
            st.success("Файлы успешно сохранены!")
        
        with st.spinner("Выполняется анализ. Это может занять несколько минут..."):
            try:
                # Запускаем main.py
                result = subprocess.run(
                    ["python", str(BASE_DIR / "main.py")], 
                    capture_output=True, 
                    text=True
                )
                
                if result.returncode != 0:
                    st.error("Ошибка при выполнении анализа:")
                    st.code(result.stderr)
                else:
                    st.success("Анализ успешно завершен!")
                    time.sleep(2)  # Даем время на генерацию отчетов
                    
                    # Показываем отчет
                    st.markdown("---")
                    st.subheader("📄 Итоговый отчет")
                    
                    report_path = REPORTS_DIR / "final_report.html"
                    if report_path.exists():
                        html_report = embed_html_report(report_path)
                        if html_report:
                            st.components.v1.html(html_report, height=1200, scrolling=True)
                    else:
                        st.error("Отчет не найден. Проверьте логи выполнения.")
            
            except Exception as e:
                st.error(f"Произошла ошибка: {str(e)}")
                st.code(traceback.format_exc())

# Инструкция, если файлы не загружены
else:
    st.info("ℹ️ Пожалуйста, загрузите оба файла для начала анализа")
    
    with st.expander("Требования к данным"):
        st.markdown("""
        **client_data.csv должен содержать столбцы:**
        - `client_id` - идентификатор клиента
        - `purchase_date` - дата покупки
        - `purchase_amount` - сумма покупки
        - `transaction_id` - ID транзакции
        - `age` - возраст клиента
        - `gender` - пол клиента
        - `region` - регион клиента
        - `traffic_source` - источник трафика
        - `last_visit_date` - дата последнего визита
        - `page_views` - количество просмотров страниц
        - `cart_adds` - добавления в корзину

        **marketing_spend.csv должен содержать столбцы:**
        - `date` - дата
        - `platform` - рекламная платформа
        - `spend` - затраты
        - `impressions` - показы
        - `clicks` - клики
        """)