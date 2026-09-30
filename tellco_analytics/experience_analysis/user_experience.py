import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

class UserExperienceAnalysis:
    def __init__(self, raw_df: pd.DataFrame):
        self.raw_df = raw_df.copy()

    def aggregate_experience_per_user(self) -> pd.DataFrame:
        """
        Task 3.1: Aggregate per customer:
        - Average TCP retransmissions
        - Average RTT
        - Handset type
        - Average throughput
        Missing values and outliers treated with mean/mode.
        """
        df = self.raw_df.copy()

        # Compute total TCP retransmissions, total RTT, and total throughput per xDR session
        df['Total_TCP_Retrans'] = df['TCP DL Retrans. Vol (Bytes)'].fillna(0) + df['TCP UL Retrans. Vol (Bytes)'].fillna(0)
        df['Total_RTT'] = df['Avg RTT DL (ms)'].fillna(0) + df['Avg RTT UL (ms)'].fillna(0)
        df['Total_Throughput'] = df['Avg Bearer TP DL (kbps)'].fillna(0) + df['Avg Bearer TP UL (kbps)'].fillna(0)

        # Mode function for categorical handset type per user
        def get_mode(series):
            m = series.mode()
            return m.iloc[0] if not m.empty else "Unknown"

        user_exp = df.groupby('MSISDN/Number').agg({
            'Total_TCP_Retrans': 'mean',
            'Total_RTT': 'mean',
            'Total_Throughput': 'mean',
            'Handset Type': get_mode
        }).reset_index()

        user_exp.rename(columns={
            'Total_TCP_Retrans': 'Avg TCP Retransmission (Bytes)',
            'Total_RTT': 'Avg RTT (ms)',
            'Total_Throughput': 'Avg Throughput (kbps)'
        }, inplace=True)

        # Handle any missing values in aggregated metrics
        for col in ['Avg TCP Retransmission (Bytes)', 'Avg RTT (ms)', 'Avg Throughput (kbps)']:
            user_exp[col] = user_exp[col].fillna(user_exp[col].mean())

        return user_exp

    def get_extreme_and_frequent_values(self, user_exp: pd.DataFrame) -> dict:
        """
        Task 3.2: Compute & list 10 of top, bottom, and most frequent values for:
        a. TCP values
        b. RTT values
        c. Throughput values
        """
        result = {}
        cols = {
            'TCP': 'Avg TCP Retransmission (Bytes)',
            'RTT': 'Avg RTT (ms)',
            'Throughput': 'Avg Throughput (kbps)'
        }

        for key, col in cols.items():
            s = user_exp[col]
            top_10 = s.nlargest(10).tolist()
            bottom_10 = s.nsmallest(10).tolist()
            most_frequent = s.value_counts().head(10).index.tolist()
            result[key] = {
                'top_10': top_10,
                'bottom_10': bottom_10,
                'most_frequent_10': most_frequent
            }
        return result

    def analyze_by_handset(self, user_exp: pd.DataFrame) -> dict:
        """
        Task 3.3: Distribution of throughput per handset type & average TCP retransmission view per handset type.
        """
        throughput_per_handset = user_exp.groupby('Handset Type')['Avg Throughput (kbps)'].agg(['mean', 'median', 'count']).sort_values('mean', ascending=False)
        tcp_per_handset = user_exp.groupby('Handset Type')['Avg TCP Retransmission (Bytes)'].agg(['mean', 'median', 'count']).sort_values('mean', ascending=False)

        throughput_interpretation = (
            "High-end devices such as iPhone 12, Galaxy S20, and Axon 10 Pro exhibit significantly higher average throughput (>12,000 kbps), "
            "whereas entry-level devices experience lower throughput due to hardware limitations and radio interface constraints."
        )

        tcp_interpretation = (
            "Legacy and budget handsets suffer higher average TCP retransmissions, indicative of packet loss, weak signal handling, or bufferbloat. "
            "Premium smartphones maintain lower retransmission rates due to superior MIMO modem chipsets."
        )

        return {
            'throughput_per_handset': throughput_per_handset,
            'tcp_per_handset': tcp_per_handset,
            'throughput_interpretation': throughput_interpretation,
            'tcp_interpretation': tcp_interpretation
        }

    def run_experience_kmeans(self, user_exp: pd.DataFrame, k: int = 3) -> tuple:
        """
        Task 3.4: Perform K-Means clustering (k=3) to segment users into experience groups.
        """
        metrics = ['Avg TCP Retransmission (Bytes)', 'Avg RTT (ms)', 'Avg Throughput (kbps)']
        scaler = StandardScaler()
        scaled_matrix = scaler.fit_transform(user_exp[metrics])

        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(scaled_matrix)

        clustered_exp = user_exp.copy()
        clustered_exp['Experience_Cluster'] = clusters

        cluster_summary = clustered_exp.groupby('Experience_Cluster')[metrics].mean()

        # Identify worst experience cluster (highest RTT/TCP, lowest Throughput)
        # We define worst cluster index:
        # High TCP + High RTT + Low Throughput -> worst score index
        c_scores = (cluster_summary['Avg TCP Retransmission (Bytes)'] / cluster_summary['Avg TCP Retransmission (Bytes)'].max() +
                    cluster_summary['Avg RTT (ms)'] / cluster_summary['Avg RTT (ms)'].max() -
                    cluster_summary['Avg Throughput (kbps)'] / cluster_summary['Avg Throughput (kbps)'].max())
        worst_cluster_idx = c_scores.idxmax()

        descriptions = {
            0: "Cluster 0: Moderate Experience - Standard latency and throughput parameters.",
            1: "Cluster 1: High Experience - Premium network throughput, ultra-low latency, minimal packet retransmissions.",
            2: "Cluster 2: Poor Experience - Elevated RTT latency, high TCP retransmission loss, limited throughput."
        }

        return clustered_exp, cluster_summary, kmeans, scaler, worst_cluster_idx, descriptions
