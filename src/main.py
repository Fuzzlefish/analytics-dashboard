from src.data.data_loader import get_data
from src.data.processor import process_data
if __name__ == "__main__":
    df = get_data("sample", refresh=True)
    print(df.head())
    df = process_data(df)
    print(df.head())

