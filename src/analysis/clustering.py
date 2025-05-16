import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import os

def perform_clustering():
    # Загрузка RFM данных
    rfm = pd.read_csv('data/processed/rfm_data.csv')
    
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm[['recency', 'frequency', 'monetary']])
    
    kmeans = KMeans(n_clusters=4, random_state=42)
    clusters = kmeans.fit_predict(rfm_scaled)
    
    rfm['cluster'] = clusters
    
    rfm.to_csv('data/processed/clusters.csv', index=False)
    
    return rfm

if __name__ == '__main__':
    perform_clustering()

    