from src.data.stock_downloader import StockDownloader
from src.data.stock_combiner import StockCombiner
from src.config import TICKERS

if __name__ == "__main__":
    downloader = StockDownloader(
        tickers=TICKERS,
        period="10y",
        interval="1d",
        out_dir="data/"
    )
    files = downloader.download()
    combined_csv = StockCombiner(files, out_dir="data/").combine()
    print(f"Combined CSV saved to: {combined_csv}")
