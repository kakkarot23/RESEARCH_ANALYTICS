import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

class UserSatisfactionAnalysis:
    def __init__(self, engagement_df: pd.DataFrame, experience_df: pd.DataFrame):
        self.eng_df = engagement_df.copy()
        self.exp_df = experience_df.copy()
        self.merged_df = None

    def merge_features(self) -> pd.DataFrame:
        """Merges engagement and experience datasets on MSISDN/Number."""
        self.merged_df = pd.merge(self.eng_df, self.exp_df, on='MSISDN/Number', how='inner')
        return self.merged_df

    def compute_scores(self, eng_kmeans, eng_scaler, less_engaged_cluster_idx,
                       exp_kmeans, exp_scaler, worst_exp_cluster_idx) -> pd.DataFrame:
        """
        Task 4.1 & 4.2:
        a. Engagement score: Euclidean distance to less engaged cluster centroid
        b. Experience score: Euclidean distance to worst experience cluster centroid
        c. Satisfaction score: Average of engagement score and experience score
        """
        if self.merged_df is None:
            self.merge_features()

        eng_metrics = ['xDR Sessions', 'Total Duration (ms)', 'Total Traffic (Bytes)']
        exp_metrics = ['Avg TCP Retransmission (Bytes)', 'Avg RTT (ms)', 'Avg Throughput (kbps)']

        # Scaled feature matrices
        eng_scaled = eng_scaler.transform(self.merged_df[eng_metrics])
        exp_scaled = exp_scaler.transform(self.merged_df[exp_metrics])

        # Centroids
        less_engaged_centroid = eng_kmeans.cluster_centers_[less_engaged_cluster_idx].reshape(1, -1)
        worst_exp_centroid = exp_kmeans.cluster_centers_[worst_exp_cluster_idx].reshape(1, -1)

        # Euclidean distances
        eng_scores = cdist(eng_scaled, less_engaged_centroid, metric='euclidean').flatten()
        exp_scores = cdist(exp_scaled, worst_exp_centroid, metric='euclidean').flatten()

        self.merged_df['Engagement_Score'] = eng_scores
        self.merged_df['Experience_Score'] = exp_scores
        self.merged_df['Satisfaction_Score'] = (eng_scores + exp_scores) / 2.0

        return self.merged_df

    def get_top_satisfied_customers(self, top_n: int = 10) -> pd.DataFrame:
        """Task 4.2: Report top 10 satisfied customers."""
        return self.merged_df.nlargest(top_n, 'Satisfaction_Score')[
            ['MSISDN/Number', 'Engagement_Score', 'Experience_Score', 'Satisfaction_Score']
        ]

    def build_regression_model(self, model_type: str = "rf") -> dict:
        """
        Task 4.3: Build regression model to predict satisfaction score.
        """
        feature_cols = ['xDR Sessions', 'Total Duration (ms)', 'Total Traffic (Bytes)',
                        'Avg TCP Retransmission (Bytes)', 'Avg RTT (ms)', 'Avg Throughput (kbps)',
                        'Engagement_Score', 'Experience_Score']
        X = self.merged_df[feature_cols]
        y = self.merged_df['Satisfaction_Score']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        if model_type == "rf":
            model = RandomForestRegressor(n_estimators=100, random_state=42)
        else:
            model = LinearRegression()

        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        mse = mean_squared_error(y_test, predictions)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, predictions)

        return {
            'model': model,
            'mse': mse,
            'rmse': rmse,
            'r2_score': r2,
            'feature_names': feature_cols
        }

    def run_satisfaction_kmeans(self, k: int = 2) -> tuple:
        """
        Task 4.4 & 4.5:
        Run K-Means (k=2) on engagement & experience scores and aggregate average scores.
        """
        scores_matrix = self.merged_df[['Engagement_Score', 'Experience_Score']]
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(scores_matrix)

        self.merged_df['Satisfaction_Cluster'] = clusters
        cluster_summary = self.merged_df.groupby('Satisfaction_Cluster').agg({
            'Engagement_Score': 'mean',
            'Experience_Score': 'mean',
            'Satisfaction_Score': 'mean',
            'MSISDN/Number': 'count'
        }).reset_index()

        cluster_summary.rename(columns={'MSISDN/Number': 'User_Count'}, inplace=True)
        return self.merged_df, cluster_summary, kmeans
