import sqlite3
import pandas as pd
import os
from sqlalchemy import create_engine

class TellcoDatabaseExporter:
    def __init__(self, db_path: str = "data/tellco_analytics.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.db_url = f"sqlite:///{self.db_path}"
        self.engine = create_engine(self.db_url)

    def export_user_scores(self, df: pd.DataFrame, table_name: str = "user_satisfaction_scores") -> str:
        """
        Exports the user dataframe containing MSISDN/Number, Engagement_Score, 
        Experience_Score, and Satisfaction_Score to the database.
        """
        cols_to_export = ['MSISDN/Number', 'Engagement_Score', 'Experience_Score', 'Satisfaction_Score']
        if 'Satisfaction_Cluster' in df.columns:
            cols_to_export.append('Satisfaction_Cluster')

        export_df = df[cols_to_export].copy()
        export_df.to_sql(table_name, con=self.engine, if_exists='replace', index=False)
        return f"Successfully exported {len(export_df)} user records to table '{table_name}' in SQLite DB at {self.db_path}."

    def execute_select_query(self, query: str = "SELECT * FROM user_satisfaction_scores LIMIT 10;") -> pd.DataFrame:
        """
        Executes a SQL SELECT query against the local database and returns results as DataFrame.
        """
        with self.engine.connect() as conn:
            result_df = pd.read_sql(query, con=conn)
        return result_df
