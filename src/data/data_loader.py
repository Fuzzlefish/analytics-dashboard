import pandas as pd

from src.config import DATASETS


class InterfaceDataLoader:
    """ Interface for data loading for different data sources"""
    def load_data(self, refresh: bool = False):
        """Load the dataset from a file"""
        raise NotImplementedError


class CSVDataLoader(InterfaceDataLoader):
    """Data loader for CSV files with caching"""
    def __init__(self, path):
        self.path = path
        self._data = None
    def load_data(self, refresh: bool = False) -> pd.DataFrame:
        """Load data from a CSV file

        Args:
            refresh: bool = False (if true, forces reload from disk)

        Returns:
            pd.DataFrame
        """
        if not refresh and self._data is not None:
            print("Returning cached data...")
            return self._data

        print(f"Loading data from {self.path}...")
        self._data = pd.read_csv(self.path)
        print("Data loaded successfully.")
        return self._data


def get_data(name: str = "sample", refresh: bool = False):
    """Loads a dataset by name from the config
    
    Args: 
        name: str = "sample" (name of the dataset to load)
        refresh: bool = False (if true, forces reload from disk)

    Returns:
        pd.DataFrame : the loaded dataset
    """
    if name not in DATASETS:
        raise ValueError(f"Dataset {name} not found")
    path = DATASETS[name]
    loader = CSVDataLoader(path)
    return loader.load_data(refresh=refresh)

