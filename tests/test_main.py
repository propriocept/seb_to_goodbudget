"""Tests for main module."""

from datetime import datetime
from decimal import Decimal
import pandas as pd
from pathlib import Path
import pytest

import seb_to_goodbudget.main as M

fixture_input_filenames = [
    "tests/fixtures/test_input.xlsx",
    Path("tests/fixtures/test_input.xlsx"),
]


@pytest.mark.parametrize("filename", fixture_input_filenames)
def test_read_excel(filename):
    """Output should be a pandas dataframe with
    Date : datetime64
    Name : str
    Amount : Decimal
    """
    expected = pd.DataFrame(
        [
            {
                "Date": datetime(year=2023, month=10, day=6),
                "Name": "Transaction 1",
                "Amount": Decimal(-9999.00),
            },
            {
                "Date": datetime(year=2023, month=10, day=3),
                "Name": "Transaction 2",
                "Amount": Decimal(-2.00),
            },
            {
                "Date": datetime(year=2023, month=10, day=3),
                "Name": "Transaction 3",
                "Amount": Decimal(10001.00),
            },
        ]
    )
    actual = M.read_excel(filename)
    pd.testing.assert_frame_equal(expected, actual)


def test_write_csv_creates_file(tmp_path):
    """Does the function create a file with the expected filename?"""
    df_output = pd.DataFrame(
        [
            {
                "Date": datetime(year=2023, month=10, day=6),
                "Name": "Transaction 1",
                "Amount": Decimal(-9999.00),
            },
            {
                "Date": datetime(year=2023, month=10, day=3),
                "Name": "Transaction 2",
                "Amount": Decimal(-2.00),
            },
            {
                "Date": datetime(year=2023, month=10, day=3),
                "Name": "Transaction 3",
                "Amount": Decimal(10001.00),
            },
        ]
    )
    test_filename = tmp_path / "test_file.csv"
    M.write_csv(df=df_output, filename=test_filename)
    assert test_filename.exists()

