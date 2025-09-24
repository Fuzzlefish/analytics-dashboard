from pathlib import Path
import pandas as pd
class StockCombiner:

    """Combine multiple stock csv files into one dataframe."""

    def __init__(self, files, out_dir="data/"):
        """
        Initialises a StockCombiner object.

        Args:
            files (list[str]): A list of paths to the CSV files to combine.
            out_dir (str, optional): The directory where the combined CSV file will be saved. Defaults to "data/".

        Returns:
            None
        """
        self.files = files
        self.out_dir = Path(out_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)

    def combine(self):
        """
        Combine multiple stock csv files into one dataframe.

        For each CSV file, parse the "Date" column, add a "Ticker" column with the ticker symbol from the filename, and then concatenate all the dataframes together.

        Args:
            None

        Returns:
            str: The path to the combined CSV file.
        """
        frames = []
        for file in self.files:
            df = pd.read_csv(file, parse_dates=["Date"])
            ticker = Path(file).stem.replace("_stock", "") # Get the ticker from the filename
            df["Ticker"] = ticker
            frames.append(df)
        combined = pd.concat(frames, ignore_index=True)
        return self.save(combined)

    def save(self, combined):
        """Save the combined dataframe to a CSV file.
        
        Args:
            combined (pd.DataFrame): The combined dataframe to save.
        
        Returns:
            str: The path to the saved CSV file.
        """
        combined_path = self.out_dir / "combined_stock.csv"
        combined.to_csv(combined_path, index=False)
        return combined_path