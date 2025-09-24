import pandas as pd
import numpy as np
import pytest
from src.data.processor import (
    standardise_column_names,
    drop_duplicates,
    fill_missing,
    convert_types,
    remove_outliers,
    process_data
)

# Sample DataFrame fixture
@pytest.fixture
def sample_df():
    return pd.DataFrame({
        " Date ": ["2025-06-05", "2025-06-06", "2025-06-06"],
        "Open": [100, 200, np.nan],
        "Close": [110, 210, np.nan],
        "Ticker": ["AAPL", "AAPL", "AAPL"]
    })


def test_standardise_column_names(sample_df):
    df = standardise_column_names(sample_df)
    assert list(df.columns) == ["date", "open", "close", "ticker"]


def test_drop_duplicates(sample_df):
    df = drop_duplicates(sample_df)
    # Third row has NaN, so considered distinct → 3 rows remain
    assert df.shape[0] == 3


def test_fill_missing(sample_df):
    df = fill_missing(sample_df)
    # Numeric NaNs filled with 0
    assert df.loc[2, "Open"] == 0
    assert df.loc[2, "Close"] == 0
    # Object column remains unchanged
    assert df.loc[2, "Ticker"] == "AAPL"


def test_convert_types(sample_df):
    df = standardise_column_names(sample_df)
    df = convert_types(df)
    assert pd.api.types.is_datetime64_any_dtype(df["date"])
    assert pd.api.types.is_numeric_dtype(df["open"])
    assert pd.api.types.is_numeric_dtype(df["close"])
    # Ticker stays as object type
    assert df["ticker"].dtype == object


def test_remove_outliers():
    df = pd.DataFrame({"value": [1, 2, 3, 1000]})
    df_clean = remove_outliers(df)
    assert 1000 not in df_clean["value"].values
    assert df_clean.shape[0] == 3


def test_process_data(sample_df):
    df_clean = process_data(sample_df)
    assert "date" in df_clean.columns
    assert pd.api.types.is_datetime64_any_dtype(df_clean["date"])
    # After cleaning, row count matches updated fixture
    assert df_clean.shape[0] == 3
