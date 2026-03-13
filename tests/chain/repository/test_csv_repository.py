import csv
from pathlib import Path

from reporter.chain.repository.csv_repository import CSVRepository


def test_csv_repository_reads_correctly(tmp_path: Path):
    test_file = tmp_path / "test_data.csv"

    with open(test_file, mode="w", encoding="utf8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["student", "date", "coffee_spent"])
        writer.writerow(["Alice", "2023-10-01", "3"])
        writer.writerow(["Bob", "2023-10-02", "5"])

    repo = CSVRepository()
    data = repo.get_source_data(test_file)

    assert len(data) == 2
    assert data[0] == {"student": "Alice", "date": "2023-10-01", "coffee_spent": "3"}
    assert data[1] == {"student": "Bob", "date": "2023-10-02", "coffee_spent": "5"}
