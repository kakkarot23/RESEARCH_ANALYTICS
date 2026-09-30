import os
import pandas as pd

from tellco_analytics.data_processing.cleaner import TellcoDataCleaner
from tellco_analytics.overview_analysis.user_overview import UserOverviewAnalysis
from tellco_analytics.engagement_analysis.user_engagement import UserEngagementAnalysis
from tellco_analytics.experience_analysis.user_experience import UserExperienceAnalysis
from tellco_analytics.satisfaction_analysis.user_satisfaction import UserSatisfactionAnalysis
from tellco_analytics.database.exporter import TellcoDatabaseExporter
from tellco_analytics.ml_tracking.tracker import ModelTracker

def main():
    print("=== Starting TellCo Telecommunication Analytics Pipeline ===")
    
    # 0. Load Data
    data_path = os.path.join("d:/PROJECT 1", "data", "telecom_xDR_data.csv")
    if not os.path.exists(data_path):
        from scripts.generate_data import generate_tellco_data
        generate_tellco_data()

    raw_df = pd.read_csv(data_path)
    print(f"[Data Loading] Loaded {len(raw_df)} records.")

    # 1. Clean Data & Treat Outliers/Missing
    cleaner = TellcoDataCleaner(raw_df)
    clean_df = cleaner.handle_missing_values()
    clean_df = cleaner.treat_outliers_iqr()
    feature_store_path = cleaner.save_feature_store("data/cleaned_telecom_data.csv")
    print(f"[Task 0] Cleaned data and stored features at {feature_store_path}")

    # 2. Task 1: User Overview Analysis
    overview = UserOverviewAnalysis(clean_df)
    top_10_handsets = overview.get_top_handsets(10)
    top_3_mfg = overview.get_top_manufacturers(3)
    top_5_per_mfg = overview.get_top_handsets_per_top_manufacturers()
    user_agg = overview.aggregate_per_user()
    dispersion_params = overview.compute_dispersion_parameters(user_agg)
    decile_summary = overview.decile_segmentation(user_agg)
    corr_matrix = overview.compute_app_correlation(user_agg)
    pca_results = overview.perform_pca(user_agg)

    print("\n--- Task 1 Summary ---")
    print("Top 3 Manufacturers:\n", top_3_mfg)
    print("Aggregated User Count:", len(user_agg))

    # 3. Task 2: User Engagement Analysis
    engagement = UserEngagementAnalysis(user_agg, clean_df)
    top_10_eng = engagement.get_top_10_per_metric()
    eng_clustered_df, eng_stats, eng_kmeans, eng_scaler = engagement.run_kmeans_clustering(k=3)
    top_3_apps = engagement.get_top_used_apps(3)
    elbow_results = engagement.calculate_elbow_method()

    # Identify less engaged cluster (index with lowest average session count & traffic)
    c_traffic_means = eng_stats['Total Traffic (Bytes)']['mean']
    less_engaged_idx = c_traffic_means.idxmin()

    print("\n--- Task 2 Summary ---")
    print("Top 3 Used Apps:\n", top_3_apps)
    print(f"Less Engaged Cluster Index: {less_engaged_idx}")

    # 4. Task 3: Experience Analytics
    experience = UserExperienceAnalysis(clean_df)
    user_exp = experience.aggregate_experience_per_user()
    extreme_frequent = experience.get_extreme_and_frequent_values(user_exp)
    handset_exp_summary = experience.analyze_by_handset(user_exp)
    exp_clustered_df, exp_stats, exp_kmeans, exp_scaler, worst_exp_idx, exp_desc = experience.run_experience_kmeans(user_exp, k=3)

    print("\n--- Task 3 Summary ---")
    print(f"Worst Experience Cluster Index: {worst_exp_idx}")

    # 5. Task 4: Satisfaction Analysis & ML Model
    satisfaction = UserSatisfactionAnalysis(eng_clustered_df, exp_clustered_df)
    merged_scores_df = satisfaction.compute_scores(
        eng_kmeans, eng_scaler, less_engaged_idx,
        exp_kmeans, exp_scaler, worst_exp_idx
    )
    top_10_satisfied = satisfaction.get_top_satisfied_customers(10)
    regression_res = satisfaction.build_regression_model(model_type="rf")
    sat_clustered_df, sat_summary, sat_kmeans = satisfaction.run_satisfaction_kmeans(k=2)

    print("\n--- Task 4 Summary ---")
    print(f"Random Forest Regression R2 Score: {regression_res['r2_score']:.4f}")
    print(f"Random Forest RMSE: {regression_res['rmse']:.4f}")

    # 6. Task 4.6: Database Export
    db_exporter = TellcoDatabaseExporter("data/tellco_analytics.db")
    export_msg = db_exporter.export_user_scores(merged_scores_df, "user_satisfaction_scores")
    print(f"\n[Database Exporter] {export_msg}")
    sample_query_df = db_exporter.execute_select_query("SELECT * FROM user_satisfaction_scores LIMIT 5;")
    print("Sample SQL Select Query Output:\n", sample_query_df)

    # 7. Task 4.7: MLOps Model Tracking
    tracker = ModelTracker("artifacts/mlops_tracking")
    run_ctx = tracker.start_run("TellCo_Satisfaction_RF_Run", source="scripts/run_pipeline.py", code_version="v1.0.0")
    logged_run = tracker.log_run(
        run_ctx=run_ctx,
        parameters={"n_estimators": 100, "random_state": 42, "model_type": "RandomForestRegressor"},
        metrics={"r2_score": regression_res['r2_score'], "rmse": regression_res['rmse'], "mse": regression_res['mse']},
        model_object=regression_res['model'],
        artifact_paths=["data/cleaned_telecom_data.csv", "data/tellco_analytics.db"]
    )
    print(f"\n[MLOps Tracker] Logged run ID {logged_run['run_id']} with R2={regression_res['r2_score']:.4f}")

    print("\n=== TellCo Analytics Pipeline Completed Successfully! ===")

if __name__ == "__main__":
    main()
