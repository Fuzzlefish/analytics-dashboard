import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def plot_stock_line(df: pd.DataFrame, ticker: str) -> go.Figure:
    """
    Plot historical closing prices for a single stock.
    """
    df_ticker = df[df["ticker"] == ticker]
    fig = px.line(
        df_ticker,
        x="date",
        y="close",
        title=f"{ticker} Close Prices"
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Close Price",
        template="plotly_white"
    )
    return fig


def plot_stock_with_prediction(df: pd.DataFrame, ticker: str, predicted: list) -> go.Figure:
    """
    Plot historical closing prices and overlay predicted future prices.
    
    Args:
        df (pd.DataFrame): Cleaned stock DataFrame.
        ticker (str): Stock ticker symbol.
        predicted (list[float]): Predicted closing prices for future days.
    """
    df_ticker = df[df["ticker"] == ticker].copy()
    last_date = df_ticker["date"].max()
    future_dates = pd.date_range(
        start=last_date + pd.Timedelta(days=1),
        periods=len(predicted),
        freq='D'
    )
    df_pred = pd.DataFrame({"date": future_dates, "close": predicted})

    fig = go.Figure()
    # Historical prices
    fig.add_trace(go.Scatter(
        x=df_ticker["date"],
        y=df_ticker["close"],
        mode="lines",
        name="Historical"
    ))
    # Predicted prices
    fig.add_trace(go.Scatter(
        x=df_pred["date"],
        y=df_pred["close"],
        mode="lines+markers",
        name="Predicted",
        line=dict(dash="dash", color="red")
    ))

    fig.update_layout(
        title=f"{ticker} Close Prices & Predictions",
        xaxis_title="Date",
        yaxis_title="Close Price",
        template="plotly_white"
    )
    return fig


def plot_combined_stocks(df: pd.DataFrame) -> go.Figure:
    """
    Plot closing prices for multiple stocks in a single chart.
    
    Args:
        df (pd.DataFrame): Cleaned combined stock DataFrame.
    """
    fig = px.line(
        df,
        x="date",
        y="close",
        color="ticker",
        title="Combined Stock Close Prices"
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Close Price",
        template="plotly_white"
    )
    return fig
