import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import os

# Настройка Faker для русскоязычных данных
fake = Faker('ru_RU')

# Параметры генерации
NUM_CLIENTS = 5000  # Количество уникальных клиентов
MAX_TRANSACTIONS_PER_CLIENT = 10  # Макс. число транзакций на клиента
START_DATE = datetime(2023, 1, 1)  # Начальная дата для генерации транзакций
END_DATE = datetime(2025, 3, 31)  # Конечная дата для данных

# Создаем папку data/raw если её нет
os.makedirs('data/raw', exist_ok=True)

# Списки для генерации
regions = ['Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург', 'Казань']
traffic_sources = ['Яндекс.Директ', 'Google Ads', 'ВКонтакте', 'Поиск (organic)', 'Email-рассылка']
genders = ['М', 'Ж']

# 1. Генерация клиентских данных
print("Генерация клиентских данных...")
client_data = []
for client_num in range(1, NUM_CLIENTS + 1):
    client_id = f'user_{client_num}'
    age = random.randint(18, 70)
    gender = random.choice(genders)
    region = random.choice(regions)
    traffic_source = random.choice(traffic_sources)
    
    # Генерация данных о посещениях
    last_visit_date = fake.date_between(start_date='-30d', end_date='today')
    page_views = random.randint(1, 50)
    cart_adds = random.randint(0, 10) if random.random() > 0.3 else 0
    
    # Генерация транзакций
    num_transactions = random.randint(0, MAX_TRANSACTIONS_PER_CLIENT)
    for trans_num in range(1, num_transactions + 1):
        transaction_id = f'txn_{client_num}_{trans_num}'
        purchase_date = fake.date_between(start_date=START_DATE, end_date=END_DATE)
        purchase_amount = random.randint(300, 50000)
        
        client_data.append([
            client_id, purchase_date, purchase_amount, transaction_id,
            age, gender, region, traffic_source,
            last_visit_date, page_views, cart_adds
        ])

# Сохраняем клиентские данные
client_columns = [
    'client_id', 'purchase_date', 'purchase_amount', 'transaction_id',
    'age', 'gender', 'region', 'traffic_source',
    'last_visit_date', 'page_views', 'cart_adds'
]
client_df = pd.DataFrame(client_data, columns=client_columns)
client_path = os.path.join('data', 'raw', 'client_data.csv')
client_df.to_csv(client_path, index=False, encoding='utf-8-sig')

# 2. Генерация данных о рекламных расходах (1000 записей)
print("Генерация данных о рекламных расходах...")
marketing_data = []
for _ in range(5000):
    date = fake.date_between(start_date=START_DATE, end_date=END_DATE)
    platform = random.choice(traffic_sources)
    
    # Генерация правдоподобных значений
    spend = random.randint(1000, 100000)
    impressions = spend * random.randint(1, 3)
    clicks = int(impressions * random.uniform(0.01, 0.05))  # CTR 1-5%
    
    marketing_data.append([date, platform, spend, impressions, clicks])

# Сохраняем маркетинговые данные
marketing_df = pd.DataFrame(
    marketing_data,
    columns=['date', 'platform', 'spend', 'impressions', 'clicks']
)
marketing_path = os.path.join('data', 'raw', 'marketing_spend.csv')
marketing_df.to_csv(marketing_path, index=False, encoding='utf-8-sig')

print("\nФайлы успешно созданы в data/raw:")
print(f"- {client_path} ({len(client_df)} записей)")
print(f"- {marketing_path} ({len(marketing_df)} записей)")

# Генерация мини-версий для тестирования (по 100 записей)
if not os.path.exists('data/raw/test'):
    os.makedirs('data/raw/test')

client_df.sample(100).to_csv(
    os.path.join('data', 'raw', 'test', 'client_data_sample.csv'),
    index=False,
    encoding='utf-8-sig'
)
marketing_df.sample(100).to_csv(
    os.path.join('data', 'raw', 'test', 'marketing_spend_sample.csv'),
    index=False,
    encoding='utf-8-sig'
)
print("\nТестовые файлы (по 100 записей) созданы в data/raw/test")