import pandas as pd

df = pd.read_csv('data/raw/client_data.csv', parse_dates=['purchase_date', 'last_visit_date'])

df.drop_duplicates(inplace=True)

df = df.dropna(subset=['client_id', 'purchase_amount', 'purchase_date'])

df['cart_adds'] = df['cart_adds'].fillna(0)
df['page_views'] = df['page_views'].fillna(0)
df = df[df['purchase_amount'] > 0]

df['gender'] = df['gender'].fillna('unknown').astype('category')


df_1 = pd.read_csv('data/raw/marketing_spend.csv', parse_dates=['date'])

df_1.drop_duplicates(subset=['date', 'platform'], inplace=True)

df_1 = df_1.dropna(subset=['spend', 'impressions', 'clicks'])
df_1 = df_1[(df_1['spend'] > 0) & (df_1['impressions'] > 0) & (df_1['clicks'] > 0)]