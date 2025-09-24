import os
import pandas as pd
import pytest
from src.data.data_loader import CSVDataLoader, get_data
from src.config import DATASETS

# --- Setup a temporary CSV for testing ---
TEST_CSV_PATH = "tests/test_sample.csv"

@pytest.fixture(scope="module")
def sample_csv():
    df = pd.DataFrame({
        "col1": [1, 2, 3],
        "col2": ["a", "b", "c"]
    })
    df.to_csv(TEST_CSV_PATH, index=False)
    yield TEST_CSV_PATH
    os.remove(TEST_CSV_PATH)

# --- Tests for CSVDataLoader ---

def test_csv_loader_loads_file(sample_csv):
    loader = CSVDataLoader(sample_csv)
    df = loader.load_data()
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (3, 2)
    assert list(df.columns) == ["col1", "col2"]

def test_csv_loader_caching(sample_csv):
    loader = CSVDataLoader(sample_csv)
    df1 = loader.load_data()
    df2 = loader.load_data()  # Should use cached version
    assert df1.equals(df2)

def test_csv_loader_refresh(sample_csv):
    loader = CSVDataLoader(sample_csv)
    df1 = loader.load_data()
    df2 = loader.load_data(refresh=True)  # Forces reload
    assert df1.equals(df2)

# --- Tests for get_data function ---

def test_get_data_with_valid_name(monkeypatch, sample_csv):
    # Patch DATASETS temporarily
    monkeypatch.setitem(DATASETS, "TEST", sample_csv)
    df = get_data("TEST", refresh=True)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (3, 2)

def test_get_data_invalid_name():
    with pytest.raises(ValueError) as exc:
        get_data("NON_EXISTENT")
    assert "Dataset NON_EXISTENT not found" in str(exc.value)
