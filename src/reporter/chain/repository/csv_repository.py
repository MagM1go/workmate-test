import csv
from pathlib import Path
from typing import override

from reporter.chain.repository.base import BaseRepository


class CSVRepository(BaseRepository):
    @override
    def get_source_data(self, source: Path) -> list[dict[str, str]]:
        with source.open(encoding="utf8", newline="") as csv_file:
            return list(csv.DictReader(csv_file))
