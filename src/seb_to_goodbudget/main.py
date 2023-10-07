"""One file for all functions to begin with."""
import os

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
    in_df = pd.read_excel(io=filename, sheet_name="Sheet1", skiprows=7, header=0, dtype={"Belopp": float})
    out_df = pd.DataFrame({
        "Date": pd.to_datetime(in_df["Bokförd"]),
        "Name": in_df["Text"],
        "Amount": in_df["Belopp"],
    })
    # Convert Amount to decimals because they are currency.
    out_df["Amount"] = [Decimal(x) for x in out_df.Amount]
    return out_df


def main() -> bool:
    return True

if __name__ == "main":
    main()