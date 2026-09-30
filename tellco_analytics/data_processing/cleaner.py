import pandas as pd
import numpy as np
import os

class TellcoDataCleaner:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def handle_missing_values(self) -> pd.DataFrame:
        """
        Treats missing values: replaces missing values in numerical columns 
        with column mean and categorical columns with column mode.
        """
        for col in self.df.columns:
            if self.df[col].dtype in ['float64', 'int64', 'float32', 'int32']:
                mean_val = self.df[col].mean()
                self.df[col] = self.df[col].fillna(mean_val)
            else:
                mode_val = self.df[col].mode()[0] if not self.df[col].mode().empty else "Unknown"
                self.df[col] = self.df[col].fillna(mode_val)
        return self.df

    def treat_outliers_iqr(self, columns: list = None, factor: float = 1.5) -> pd.DataFrame:
        """
        Detects and caps outliers using the Interquartile Range (IQR) method.
        """
        if columns is None:
            columns = self.df.select_dtypes(include=[np.number]).columns.tolist()
            
        for col in columns:
            if col in self.df.columns:
                q1 = self.df[col].quantile(0.25)
                q3 = self.df[col].quantile(0.75)
                iqr = q3 - q1
                lower_bound = q1 - (factor * iqr)
                upper_bound = q3 + (factor * iqr)
                
                # Cap outliers to bounds
                self.df[col] = np.where(self.df[col] < lower_bound, lower_bound, self.df[col])
                self.df[col] = np.where(self.df[col] > upper_bound, upper_bound, self.df[col])
        return self.df

    def save_feature_store(self, output_path: str = "data/cleaned_telecom_data.parquet") -> str:
        """
        Stores processed features in a reusable parquet format for feature store usage.
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        if output_path.endswith('.parquet'):
            self.df.to_parquet(output_path, index=False)
        else:
            self.df.to_csv(output_path, index=False)
        return output_path
