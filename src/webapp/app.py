import dash
from dash import html, dcc
from dash.dependencies import Input, Output
from src.data.data_loader import get_data
from src.data.processor import process_data
from src.models.predictive_model import StockPredictor
from src.viz.charts import plot_stock_line, plot_stock_with_prediction, plot_combined_stocks

# Load and process the combined CSV
df_combined = get_data("COMBINED", refresh=True)
df_clean = process_data(df_combined)
tickers = df_clean["ticker"].unique()

# Initialize Dash
app = dash.Dash(__name__)
app.title = "Stock Analytics Dashboard"

# Layout
app.layout = html.Div([
    html.H1("Stock Analytics Dashboard", style={"textAlign": "center"}),

    html.Div([
        html.Label("Select Stock:"),
        dcc.Dropdown(
            id="ticker-dropdown",
            options=[{"label": t, "value": t} for t in tickers],
            value=tickers[0]
        ),
    ], style={"width": "250px", "margin": "20px"}),

    html.Div([
        html.Label("Predict Next Days:"),
        dcc.Slider(
            id="predict-days-slider",
            min=0,
            max=30,
            step=1,
            value=0,
            marks={i: str(i) for i in range(0, 31, 5)}
        ),
    ], style={"width": "500px", "margin": "20px"}),

    dcc.Graph(id="stock-chart"),

    html.H2("Combined Stock Comparison"),
    dcc.Graph(
        figure=plot_combined_stocks(df_clean)
    )
])

# Callback to update chart based on selected stock and prediction horizon
@app.callback(
    Output("stock-chart", "figure"),
    Input("ticker-dropdown", "value"),
    Input("predict-days-slider", "value")
)
def update_stock_chart(ticker, predict_days):
    df_ticker = df_clean[df_clean["ticker"] == ticker]

    if predict_days > 0:
        predictor = StockPredictor(lag=7)
        predictor.train(df_ticker)
        predicted_prices = predictor.predict_next_days(df_ticker, predict_days)
        fig = plot_stock_with_prediction(df_clean, ticker, predicted_prices)
    else:
        fig = plot_stock_line(df_clean, ticker)

    return fig

if __name__ == "__main__":
    app.run(debug=True)
