from src.data.stock_downloader import StockDownloader
from src.data.stock_combiner import StockCombiner
from src.data.data_loader import get_data
from src.data.processor import process_data
from src.models.predictive_model import StockPredictor

if __name__ == "__main__":
    # Download historical stock data
    downloader = StockDownloader(
        tickers=["AAPL", "MSFT", "TSLA"],
        period="1y",
        interval="1d",
        out_dir="data/"
    )
    files = downloader.download()

    # Combine individual CSVs into a single dataset
    combined_csv = StockCombiner(files, out_dir="data/").combine()

    # Load and clean the combined dataset
    df_combined = get_data("COMBINED", refresh=True)
    df_clean = process_data(df_combined)

    # Filter for a specific stock and train the predictive model
    df_aapl = df_clean[df_clean["ticker"] == "AAPL"]
    predictor = StockPredictor(lag=7)
    predictor.train(df_aapl)

    # Predict the next x days of closing prices
    next_15_days = predictor.predict_next_days(df_aapl, days=15)
    print("Next 15 days predicted Close prices for AAPL:", next_15_days)
