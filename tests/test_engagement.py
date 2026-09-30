import pytest
import pandas as pd
import numpy as np
from tellco_analytics.engagement_analysis.user_engagement import UserEngagementAnalysis

@pytest.fixture
def user_agg_df():
    return pd.DataFrame({
        'MSISDN/Number': [f"U{i}" for i in range(1, 11)],
        'xDR Sessions': [1, 5, 2, 8, 10, 3, 4, 7, 9, 6],
        'Total Duration (ms)': [100, 500, 200, 800, 1000, 300, 400, 700, 900, 600],
        'Total Traffic (Bytes)': [1000, 5000, 2000, 8000, 10000, 3000, 4000, 7000, 9000, 6000],
        'Youtube Total (Bytes)': [500, 2500, 1000, 4000, 5000, 1500, 2000, 3500, 4500, 3000],
        'Gaming Total (Bytes)': [300, 1500, 600, 2400, 3000, 900, 1200, 2100, 2700, 1800]
    })

def test_top_10_and_clustering(user_agg_df):
    eng = UserEngagementAnalysis(user_agg_df)
    top_10 = eng.get_top_10_per_metric()
    assert len(top_10['top_sessions']) == 10

    clustered, stats, kmeans, scaler = eng.run_kmeans_clustering(k=3)
    assert 'Engagement_Cluster' in clustered.columns
    assert len(set(clustered['Engagement_Cluster'])) <= 3

def test_elbow_method(user_agg_df):
    eng = UserEngagementAnalysis(user_agg_df)
    elbow = eng.calculate_elbow_method(max_k=5)
    assert len(elbow['sse']) == 5
    assert elbow['optimal_k'] == 3
