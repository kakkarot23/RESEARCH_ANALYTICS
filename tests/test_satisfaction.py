import pytest
import pandas as pd
import numpy as np
import os
from tellco_analytics.engagement_analysis.user_engagement import UserEngagementAnalysis
from tellco_analytics.experience_analysis.user_experience import UserExperienceAnalysis
from tellco_analytics.satisfaction_analysis.user_satisfaction import UserSatisfactionAnalysis
from tellco_analytics.database.exporter import TellcoDatabaseExporter
from tellco_analytics.ml_tracking.tracker import ModelTracker

@pytest.fixture
def mock_pipeline_data():
    raw_df = pd.DataFrame({
        'MSISDN/Number': [f"336{i:08d}" for i in range(1, 21)],
        'Bearer Id': [f"B{i}" for i in range(1, 21)],
        'Handset Manufacturer': ['Apple']*10 + ['Samsung']*10,
        'Handset Type': ['iPhone 12']*10 + ['Galaxy S20']*10,
        'Dur. (ms)': np.random.randint(1000, 10000, 20),
        'TCP DL Retrans. Vol (Bytes)': np.random.randint(100, 1000, 20),
        'TCP UL Retrans. Vol (Bytes)': np.random.randint(10, 100, 20),
        'Avg RTT DL (ms)': np.random.randint(10, 50, 20),
        'Avg RTT UL (ms)': np.random.randint(2, 10, 20),
        'Avg Bearer TP DL (kbps)': np.random.randint(1000, 5000, 20),
        'Avg Bearer TP UL (kbps)': np.random.randint(100, 500, 20),
        'Total DL (Bytes)': np.random.randint(10000, 50000, 20),
        'Total UL (Bytes)': np.random.randint(1000, 5000, 20),
        'Youtube Total (Bytes)': np.random.randint(5000, 20000, 20),
        'Gaming Total (Bytes)': np.random.randint(5000, 20000, 20)
    })
    return raw_df

def test_satisfaction_scores_and_db_export(mock_pipeline_data, tmp_path):
    raw_df = mock_pipeline_data
    # Aggregate engagement
    user_agg = raw_df.groupby('MSISDN/Number').agg({
        'Bearer Id': 'count',
        'Dur. (ms)': 'sum',
        'Total DL (Bytes)': 'sum',
        'Total UL (Bytes)': 'sum'
    }).reset_index()
    user_agg.rename(columns={'Bearer Id': 'xDR Sessions', 'Dur. (ms)': 'Total Duration (ms)'}, inplace=True)
    user_agg['Total Traffic (Bytes)'] = user_agg['Total DL (Bytes)'] + user_agg['Total UL (Bytes)']

    eng = UserEngagementAnalysis(user_agg)
    eng_df, eng_stats, eng_km, eng_scaler = eng.run_kmeans_clustering(k=3)

    exp = UserExperienceAnalysis(raw_df)
    user_exp = exp.aggregate_experience_per_user()
    exp_df, exp_stats, exp_km, exp_scaler, worst_exp_idx, desc = exp.run_experience_kmeans(user_exp, k=3)

    satisfaction = UserSatisfactionAnalysis(eng_df, exp_df)
    merged = satisfaction.compute_scores(eng_km, eng_scaler, 0, exp_km, exp_scaler, worst_exp_idx)

    assert 'Satisfaction_Score' in merged.columns
    assert len(merged) == 20

    top_10 = satisfaction.get_top_satisfied_customers(10)
    assert len(top_10) == 10

    reg_res = satisfaction.build_regression_model(model_type="rf")
    assert reg_res['r2_score'] >= -1.0

    # DB Exporter
    db_file = str(tmp_path / "test_tellco.db")
    exporter = TellcoDatabaseExporter(db_file)
    msg = exporter.export_user_scores(merged)
    assert "exported 20 user records" in msg

    query_df = exporter.execute_select_query("SELECT * FROM user_satisfaction_scores LIMIT 5;")
    assert len(query_df) == 5

    # MLOps Tracker
    tracker = ModelTracker(str(tmp_path / "mlops"))
    run_ctx = tracker.start_run("Test_Run")
    logged = tracker.log_run(run_ctx, {"p": 1}, {"r2": 0.99}, reg_res['model'])
    assert logged['status'] == "COMPLETED"
