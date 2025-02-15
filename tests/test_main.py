"""Tests for main module."""

from datetime import datetime
from decimal import Decimal
import pandas as pd
from pathlib import Path
import pytest
from unittest.mock import patch

from seb_to_goodbudget.main import read_excel, write_csv, main
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


def test_read_excel_file_not_found():
    """Should raise FileNotFoundError when input file doesn't exist"""
    with pytest.raises(FileNotFoundError):
        M.read_excel("nonexistent.xlsx")


def test_read_excel_invalid_format():
    """Should raise ValueError when file is not a valid Excel file"""
    with pytest.raises(ValueError):
        M.read_excel(__file__)  # Try to read the test file itself as Excel


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
        "06/10/2023,Transaction 1,-9999.00\n",
        "03/10/2023,Transaction 2,-2.00\n",
        "03/10/2023,Transaction 3,10001.00\n",
    ]
    test_filename = tmp_path / "b.csv"
    M.write_csv(df=fixture_expected_df_from_excel, filename=Path(test_filename))
    with open(test_filename, "r") as f:
        output_csv = f.readlines()
    for expected_line, actual_line in zip(expected, output_csv):
        assert expected_line == actual_line


def test_write_csv_file_exists(tmp_path, fixture_expected_df_from_excel):
    """Should raise FileExistsError when output file already exists"""
    test_filename = tmp_path / "existing.csv"
    test_filename.touch()  # Create empty file
    with pytest.raises(FileExistsError):
        M.write_csv(df=fixture_expected_df_from_excel, filename=test_filename)


def test_main_basic_conversion(tmp_path):
    """Test basic file conversion with default output name"""
    input_file = "tests/fixtures/test_input.xlsx"
    output_file = tmp_path / "test_input.csv"
    
    with patch('sys.argv', ['script', str(input_file), '-o', str(output_file)]):
        assert M.main() == 0
        assert output_file.exists()


def test_main_output_exists(tmp_path):
    """Should return 1 when output file already exists"""
    input_file = "tests/fixtures/test_input.xlsx"
    output_file = tmp_path / "existing.csv"
    output_file.touch()  # Create empty file
    
    with patch('sys.argv', ['script', str(input_file), '-o', str(output_file)]):
        assert M.main() == 1
        

def test_main_input_not_found():
    """Should return 1 when input file doesn't exist"""
    with patch('sys.argv', ['script', 'nonexistent.xlsx']):
        assert M.main() == 1


def test_main_default_output_name(tmp_path):
    """Test that default output name is input name with .csv extension"""
    input_file = tmp_path / "test.xlsx"
    # Copy test fixture to temp directory
    import shutil
    shutil.copy("tests/fixtures/test_input.xlsx", input_file)
    
    with patch('sys.argv', ['script', str(input_file)]):
        assert M.main() == 0
        assert (tmp_path / "test.csv").exists()
