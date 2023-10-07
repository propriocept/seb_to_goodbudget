"""One file for all functions to begin with."""

from decimal import Decimal
import pandas as pd
from pathlib import Path


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
    in_df = pd.read_excel(
        io=filename, sheet_name="Sheet1", skiprows=7, header=0, dtype={"Belopp": float}
    )
    out_df = pd.DataFrame(
        {
            "Date": pd.to_datetime(in_df["Bokförd"]),
            "Name": in_df["Text"],
            "Amount": in_df["Belopp"],
        }
    )
    # Convert Amount to decimals because they are currency.
    out_df["Amount"] = [Decimal(x) for x in out_df.Amount]
    return out_df


def write_csv(df: pd.DataFrame, filename: Path) -> None:
    """Write the data to format for Good Budget.

    Parameters
    ----------
    df : pd.DataFrame
        pandas dataframe with the following schema:
            Date : datetime64
            Name : str
            Amount : Decimal
    filename : pathlib.Path
        file where CSV will be written to
    """
    out_df = df.copy()
    out_df["Date"] = out_df.Date.dt.strftime(date_format="%d/%Y")
    # with open(filename, "w") as file_out:
    # file_out.write("Date,Name,Amount\n")
    # for row in out_df.itertuples():
    # file_out.write(f"{row.Date},{row.Name},{row.Amount:1.2f}")
    out_df["Amount"] = out_df.Amount.apply(lambda x: f"{x:.2f}")
    out_df.to_csv(filename, header=True, index=False, mode="x")
    return None


def main() -> bool:
    return True


if __name__ == "main":
    main()
