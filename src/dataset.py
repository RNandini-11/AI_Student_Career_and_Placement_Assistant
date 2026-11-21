import pandas as pd

from src.config import RAW_DATA


def load_data():
    """Load the raw student placement dataset."""
    df = pd.read_csv(RAW_DATA)

    print("Dataset Shape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    return df


def clean_data(df):
    """Perform basic data cleaning."""

    print("\nAfter Cleaning:")
    print("Missing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:")
    print(df.duplicated().sum())

    return df


if __name__ == "__main__":

    df = load_data()
    df = clean_data(df)

    print("\nFirst 5 Rows:")
    print(df.head())