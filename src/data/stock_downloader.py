import yfinance as yf
import pandas as pd
from pathlib import Path

class StockDownloader:
    """Download stock data from Yahoo Finance and save as CSVs."""

    def __init__(self, tickers, period="5y", interval="1mo", out_dir="../data/"):
        """
        Initialises a StockDownloader object.

        Args:
            tickers (list[str] or str): A list of ticker symbols or a single ticker symbol.
            period (str, optional): The time period for which to download data. Defaults to "5y".
            interval (str, optional): The time interval for which to download data. Defaults to "1mo".
            out_dir (str, optional): The directory where the downloaded CSV files will be saved. Defaults to "../data/".

        Returns:
            None
        """
        self.tickers = tickers if isinstance(tickers, list) else [tickers]
        self.period = period
        self.interval = interval
        self.out_dir = Path(out_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)

    def download(self):
        """Download data for each ticker and save to CSV.
        
        Args:
            None
        
        Returns:
            list[str]: A list of paths to the saved CSV files.
        """
        saved_files = []
        for ticker in self.tickers:
            data = yf.Ticker(ticker).history(period=self.period, interval=self.interval)
            filepath = self.out_dir / f"{ticker}_stock.csv"
            data.to_csv(filepath)
            saved_files.append(filepath)
            print(f"✅ Saved {ticker} data to {filepath}")
        return saved_files
