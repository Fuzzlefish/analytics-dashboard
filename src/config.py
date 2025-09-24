"""Centralised configuration for the application"""
import os

# Project directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Stock tickers to track
TICKERS = ["AAPL", "MSFT", "TSLA", "NVDA", "GOOGL", "BTC-USD"]

# Dataset registry
DATASETS = {
    "sample": os.path.join(DATA_DIR, "sample_data.csv"),
    "COMBINED": os.path.join(DATA_DIR, "combined_stock.csv"),
}

# Dynamically add each stock to the dataset registry
for ticker in TICKERS:
    DATASETS[ticker] = os.path.join(DATA_DIR, f"{ticker}_stock.csv")
