import pytest
import pandas as pd
import numpy as np
from tellco_analytics.experience_analysis.user_experience import UserExperienceAnalysis

@pytest.fixture
def raw_df():
    return pd.DataFrame({
        'MSISDN/Number': ['U1', 'U1', 'U2', 'U3'],
        'Handset Type': ['iPhone 12', 'iPhone 12', 'Galaxy S20', 'P30 Lite'],
        'TCP DL Retrans. Vol (Bytes)': [100, 200, 300, 400],
        'TCP UL Retrans. Vol (Bytes)': [10, 20, 30, 40],
        'Avg RTT DL (ms)': [20, 30, 40, 50],
        'Avg RTT UL (ms)': [5, 5, 5, 5],
        'Avg Bearer TP DL (kbps)': [5000, 6000, 7000, 8000],
        'Avg Bearer TP UL (kbps)': [500, 600, 700, 800]
    })

def test_experience_aggregation_and_kmeans(raw_df):
    exp = UserExperienceAnalysis(raw_df)
    user_exp = exp.aggregate_experience_per_user()
    assert len(user_exp) == 3  # U1, U2, U3

    extremes = exp.get_extreme_and_frequent_values(user_exp)
    assert 'TCP' in extremes
    assert len(extremes['TCP']['top_10']) > 0

    clustered_exp, summary, kmeans, scaler, worst_idx, desc = exp.run_experience_kmeans(user_exp, k=3)
    assert 'Experience_Cluster' in clustered_exp.columns
    assert worst_idx in [0, 1, 2]
