from src.data.data_loader import get_data
from src.data.processor import process_data

from src.data.stock_downloader import StockDownloader
from src.data.stock_combiner import StockCombiner

if __name__ == "__main__":

    downloader = StockDownloader(
    tickers=["AAPL", "MSFT", "TSLA"],
    period="5y",
    interval="5d",
    out_dir="data/"  # store CSVs in top-level data folder
    )
    files = downloader.download()
    combined_csv = StockCombiner(files, out_dir="data/").combine()
    df = get_data("sample", refresh=True)
    print(df.head())
    df = process_data(df)
    print(df.head())

