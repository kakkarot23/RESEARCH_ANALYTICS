import pytest
import pandas as pd
import numpy as np
import os
from tellco_analytics.data_processing.cleaner import TellcoDataCleaner

@pytest.fixture
def sample_df():
    data = {
        'col_num': [10.0, 20.0, np.nan, 200.0],
        'col_cat': ['Apple', 'Samsung', None, 'Apple']
    }
    return pd.DataFrame(data)

def test_missing_values_imputation(sample_df):
    cleaner = TellcoDataCleaner(sample_df)
    df_clean = cleaner.handle_missing_values()
    assert df_clean['col_num'].isnull().sum() == 0
    assert df_clean['col_cat'].isnull().sum() == 0
    # Mean of [10, 20, 200] = 76.6666...
    assert pytest.approx(df_clean.loc[2, 'col_num'], 0.1) == 76.666

def test_outlier_treatment_iqr():
    df = pd.DataFrame({'col_num': [10.0, 12.0, 14.0, 15.0, 16.0, 5000.0]})
    cleaner = TellcoDataCleaner(df)
    df_treated = cleaner.treat_outliers_iqr(columns=['col_num'])
    assert df_treated['col_num'].max() < 5000.0

def test_feature_store_saving(sample_df, tmp_path):
    cleaner = TellcoDataCleaner(sample_df)
    out_file = str(tmp_path / "test_store.csv")
    path = cleaner.save_feature_store(out_file)
    assert os.path.exists(path)
