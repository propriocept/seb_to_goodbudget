"""Tests for main module."""

from datetime import datetime
from decimal import Decimal
import pandas as pd
from pathlib import Path
import pytest
from typing import Generator

import seb_to_goodbudget.main as M

fixture_input_filenames = ["fixtures/test_input.xlsx", Path("fixtures/test_input.xlsx")]


@pytest.mark.parametrize('filename', fixture_input_filenames)
def test_read_excel(filename):
    """Output should be a pandas dataframe with
        Date : datetime64
        Name : str 
        Amount : Decimal
    """
    actual = M.read_excel(filename)
    expected = pd.DataFrame([
        {"Date":datetime(year=2023, month=10, day=10),"Name":"Transaction 1","Amount":Decimal(-9999)},
        {"Date":datetime(year=2023, month=10, day=3),"Name":"Transaction 2","Amount":Decimal(-2)},
        {"Date":datetime(year=2023, month=10, day=3),"Name":"Transaction 3","Amount":Decimal(10001)},
    ])
    pd.testing.assert_frame_equal(expected, actual)
