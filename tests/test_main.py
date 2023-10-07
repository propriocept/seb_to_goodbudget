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


@pytest.fixture
def fixture_expected_df_from_excel() -> pd.DataFrame:
    return pd.DataFrame(
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


@pytest.mark.parametrize("filename", fixture_input_filenames)
def test_read_excel(filename, fixture_expected_df_from_excel):
    """Output should be a pandas dataframe with
    Date : datetime64
    Name : str
    Amount : Decimal
    """
    expected = fixture_expected_df_from_excel
    actual = M.read_excel(filename)
    pd.testing.assert_frame_equal(expected, actual)


def test_write_csv_creates_file(tmp_path, fixture_expected_df_from_excel):
    """Does the function create a file with the expected filename?"""
    df_output = fixture_expected_df_from_excel
    test_filename = tmp_path / "test_file.csv"
    M.write_csv(df=df_output, filename=test_filename)
    assert test_filename.exists()


def test_write_csv_correct_format(tmp_path, fixture_expected_df_from_excel):
    """Is the output file in the expected format?"""
    expected = [
        "Date,Name,Amount\n",
        "10/06/2023,Transaction 1,-9999.00\n",
        "10/03/2023,Transaction 2,-2.00\n",
        "10/03/2023,Transaction 3,10001.00\n",
    ]
    test_filename = tmp_path / "b.csv"
    M.write_csv(df=fixture_expected_df_from_excel, filename=Path(test_filename))
    with open(test_filename, "r") as f:
        output_csv = f.readlines()
    for expected_line, actual_line in zip(expected, output_csv):
        assert expected_line == actual_line
