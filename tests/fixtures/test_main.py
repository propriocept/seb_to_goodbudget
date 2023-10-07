"""Tests for main module."""

from pathlib import Path
import pytest

import seb_to_goodbudget.main as M

test_input_filename_str: str = "fixtures/test_input.xlsx"
test_input_filename_pathlib_path: Path = Path("fixtures/test_input.xlsx")

def test_read_excel_output_schema():
    """Output should be a pandas dataframe with
        Date : datetime64
        Name : str
        Amount : Decimal
    """
    assert False

def test_read_excel_correct_content():
    """Does the output dataframe match what we expect?"""
    assert False