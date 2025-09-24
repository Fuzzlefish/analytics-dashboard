import pandas as pd


def standardise_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardise the column names of a DataFrame

    Column names are stripped of whitespace, converted to lowercase, and
    spaces are replaced with underscores.

    Args:
        df (pd.DataFrame) : The DataFrame in which to standardise column names

    Returns:
        pd.DataFrame : the DataFrame with standardised column names
    """
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    return df


def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drop duplicate rows from a DataFrame

    Args:
        df (pd.DataFrame): The DataFrame from which to drop duplicates

    Returns:
        pd.DataFrame : the DataFrame with duplicates dropped
    """
    return df.drop_duplicates()


def fill_missing(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fill missing values in a DataFrame

    Numeric columns are filled with 0, while object columns are filled with "Unknown"

    Args:
        df (pd.DataFrame) : The DataFrame in which to fill missing values

    Returns:
        pd.DataFrame : the DataFrame with missing values filled
    """
    numeric_cols = df.select_dtypes(include=["number"]).columns
    df[numeric_cols] = df[numeric_cols].fillna(0)
    
    cat_cols = df.select_dtypes(include=["object"]).columns
    df[cat_cols] = df[cat_cols].fillna("Unknown")
    
    return df


def convert_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert column types in a DataFrame:
    - Columns named "date" (case-insensitive) are converted to datetime (UTC).
    - Object columns are converted to numeric if possible, unless clearly categorical (like Ticker).

    Args:
        df (pd.DataFrame) : The DataFrame in which to convert column types

    Returns:
        pd.DataFrame : the DataFrame with column types converted
    """
    for col in df.select_dtypes(include=["object"]).columns:
        # Handle dates explicitly
        if col.lower() == "date":
            df[col] = pd.to_datetime(df[col], errors="coerce", utc=True)
        
        # Skip known categorical/string columns
        elif col.lower() in ["ticker", "symbol", "name"]:
            continue  

        # Try converting the rest to numeric
        else:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df
def remove_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove outliers from a DataFrame

    For each numeric column, find the interquartile range (IQR) and remove values outside 1.5*IQR from the column

    Args:
         df (pd.DataFrame) : the DataFrame from which to remove outliers

    Returns:
        pd.DataFrame : the DataFrame with outliers removed
    """
    numeric_cols = df.select_dtypes(include=["number"]).columns
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        df = df[(df[col] >= lower) & (df[col] <= upper)]
    return df


def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process a DataFrame with a standard cleaning pipeline.

    Steps:
        1. Standardise column names
        2. Convert column types
        3. Fill missing values
        4. Drop duplicates
        5. Remove outliers

    Args:
        df (pd.DataFrame): The DataFrame to process.

    Returns:
        pd.DataFrame: The processed DataFrame.
    """
    df = standardise_column_names(df)
    df = convert_types(df)
    df = fill_missing(df)
    df = drop_duplicates(df)
    df = remove_outliers(df)
    return df
