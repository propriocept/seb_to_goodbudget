"""One file for all functions to begin with."""

from datetime import datetime
from decimal import Decimal
import pandas as pd
from pathlib import Path
from typing import Union

def read_excel(filename: str | Path) -> pd.DataFrame:
    """Reads an .xlsx file from SEB and returns transactions as a pandas dataframe.
    
    Parameters
    ----------
    filename : str, pathlib.Path
    
    Returns
    -------
    pandas.DataFrame
        Transactions from input.
            Date : datetime64
            Name : str
            Amount : Decimal
    """
    return pd.DataFrame({
        "Date": [datetime(year=2023, month=10, day=9).date],
        "Name": ["test"],
        "Amount": [Decimal(99.99)]
    })


def main() -> bool:
    return True

if __name__ == "main":
    main()