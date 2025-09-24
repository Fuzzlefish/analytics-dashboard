import pandas as pd
from sklearn.linear_model import LinearRegression

class StockPredictor:
    def __init__(self, lag=5):
        """
        Initialises a StockPredictor object.

        Args:
            lag (int, optional): The number of lag features to create from the "Close" column. Defaults to 5.

        Returns:
            None
        """
        self.lag = lag
        self.model = LinearRegression()

    def prepare_data(self, df: pd.DataFrame):
        """
        Prepare a DataFrame for training a linear regression model.

        Args:
            df (pd.DataFrame): The DataFrame to prepare.

        Returns:
            X (pd.DataFrame): The feature matrix.
            y (pd.Series): The target vector.

        Notes:
            The DataFrame is sorted by date, and lag features are created from the "Close" column.
            The lag features are created by shifting the "Close" column by 1 to `self.lag` positions.
            The resulting DataFrame is dropped of NaN values, and the feature matrix X and target vector y are returned.
        """
        df = df.copy()
        df["date"] = pd.to_datetime(df["date"], utc=True)
        df = df.sort_values("date")

        # Create lag features for "Close"
        for i in range(1, self.lag + 1):
            df[f"lag_{i}"] = df["close"].shift(i)

        df = df.dropna()
        X = df[[f"lag_{i}" for i in range(1, self.lag + 1)]]
        y = df["close"]
        return X, y

    def train(self, df: pd.DataFrame):
        """
        Train a linear regression model on a DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame to train on.

        Returns:
            None
        """
        
        X, y = self.prepare_data(df)
        self.model.fit(X, y)

    def predict_next(self, df: pd.DataFrame):
        """
        Predict the next closing price based on the given DataFrame

        Args:
            df (pd.DataFrame): The DataFrame to predict the next closing price from

        Returns:
            float: The predicted next closing price

        Notes:
            The prediction is based on the lag features created from the "Close" column of the given DataFrame.
        """
        X, _ = self.prepare_data(df)
        return self.model.predict([X.iloc[-1]])[0]
    

    def predict_next_days(self, df: pd.DataFrame, days: int):
        """
        Predict the next `days` closing prices based on the given DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame to predict the next closing prices from.
            days (int): The number of days to predict the closing prices for.

        Returns:
            list[int]: A list of the predicted next closing prices for the given number of days.

        Notes:
            The prediction is based on the lag features created from the "Close" column of the given DataFrame.
        """
        df_temp = df.copy().sort_values("date")
        predictions = []

        last_lags = df_temp["close"].values[-self.lag:].tolist()
        lag_cols = [f"lag_{i}" for i in range(1, self.lag + 1)]

        for _ in range(days):
            X_input_df = pd.DataFrame([last_lags[-self.lag:]], columns=lag_cols)
            next_close = int(self.model.predict(X_input_df)[0])
            predictions.append(next_close)
            last_lags.append(next_close)

        return predictions
