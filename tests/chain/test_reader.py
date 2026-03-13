from datetime import date
from pathlib import Path

import pytest

from reporter.chain.reader import DataReader, StudentRecord


class MockRepository:
    def __init__(self, data):
        self.data = data

    def get_source_data(self, source: Path):
        return self.data


def test_data_reader_parsing(csv_rows):
    mock_repo = MockRepository(csv_rows)
    reader = DataReader(mock_repo)

    records = reader.read(Path("dummy.csv"))

    assert len(records) == 3
    assert isinstance(records[0], StudentRecord)
    assert records[0].student == "биба"
    assert records[0].date == date(2222, 2, 22)
    assert records[0].coffee_spent == 2


def test_data_reader_value_error_on_bad_data():
    bad_data = [{"student": "Alice", "date": "bad-date-format", "coffee_spent": "two"}]
    mock_repo = MockRepository(bad_data)
    reader = DataReader(mock_repo)

    with pytest.raises(ValueError):
        reader.read(Path("dummy.csv"))
