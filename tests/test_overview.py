import pytest
import pandas as pd
import numpy as np
from tellco_analytics.overview_analysis.user_overview import UserOverviewAnalysis

@pytest.fixture
def mock_df():
    return pd.DataFrame({
        'MSISDN/Number': ['U1', 'U1', 'U2', 'U3'],
        'Bearer Id': ['B1', 'B2', 'B3', 'B4'],
        'Handset Manufacturer': ['Apple', 'Apple', 'Samsung', 'Huawei'],
        'Handset Type': ['iPhone 12', 'iPhone 12', 'Galaxy S20', 'P30 Lite'],
        'Dur. (ms)': [1000, 2000, 3000, 4000],
        'Total DL (Bytes)': [100, 200, 300, 400],
        'Total UL (Bytes)': [50, 50, 50, 50],
        'Youtube DL (Bytes)': [20, 30, 40, 50],
        'Youtube UL (Bytes)': [5, 5, 5, 5]
    })

def test_user_overview_aggregations(mock_df):
    overview = UserOverviewAnalysis(mock_df)
    top_handsets = overview.get_top_handsets(2)
    top_mfg = overview.get_top_manufacturers(2)
    user_agg = overview.aggregate_per_user()

    assert len(top_handsets) == 2
    assert 'Apple' in top_mfg.index
    assert len(user_agg) == 3  # U1, U2, U3
    # U1 total duration is 1000 + 2000 = 3000
    u1_dur = user_agg[user_agg['MSISDN/Number'] == 'U1']['Total Duration (ms)'].values[0]
    assert u1_dur == 3000

def test_pca_computation(mock_df):
    overview = UserOverviewAnalysis(mock_df)
    user_agg = overview.aggregate_per_user()
    pca_res = overview.perform_pca(user_agg, n_components=2)
    assert len(pca_res['explained_variance_ratio']) == 2
    assert len(pca_res['interpretations']) == 4
