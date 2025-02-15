"""One file for all functions to begin with."""

from argparse import ArgumentParser
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
    out_df["Date"] = out_df.Date.dt.strftime(date_format="%d/%m/%Y")
    out_df["Amount"] = out_df.Amount.apply(lambda x: f"{x:.2f}")
    out_df.to_csv(filename, header=True, index=False, mode="x")
    return None


def main() -> int:
    """Convert SEB Excel file to Good Budget CSV format.
    
    Returns
    -------
    int
        0 for success, 1 for error
    """
    parser = ArgumentParser(
        prog="SEB transaction file to CSV for Good Budget.",
        description="Converts an SEB formated excel file to a formated CSV file.",
    )
    parser.add_argument("excel_file", help="excel file of transactions from SEB.")
    parser.add_argument("--csv_file", "-o", help="Filename of CSV where you want results for Good Budget written. If no filename is given, we reuse the name of the input excel file.")
    
    try:
        args = parser.parse_args()
        if args.csv_file is None:
            file_out = Path(args.excel_file).with_suffix(".csv")
        else:
            file_out = Path(args.csv_file)
        
        if file_out.exists():
            print(f"The output file {file_out} already exists.")
            return 1
            
        df = read_excel(filename=args.excel_file)
        write_csv(df=df, filename=file_out)
        print(f"File saved to {file_out}.")
        return 0
        
    except FileNotFoundError:
        print(f"Input file not found: {args.excel_file}")
        return 1
    except ValueError as e:
        print(f"Error reading Excel file: {e}")
        return 1
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return 1
    

if __name__ == "__main__":
    main()
