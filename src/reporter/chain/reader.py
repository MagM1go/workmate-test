from dataclasses import dataclass
from datetime import date
from pathlib import Path

from reporter.chain.repository.base import BaseRepository


# Это немношко не расширяемо, но по ТЗ новые колонки добавляться не будут
# так что, считаю, привязка к одной модели не будет нарушением
@dataclass
class StudentRecord:
    student: str
    date: date
    coffee_spent: int
    sleep_hours: float
    study_hours: float
    mood: str
    exam: str


class DataReader:
    def __init__(self, repository: BaseRepository) -> None:
        self._repository = repository

    def read(self, source: Path) -> list[StudentRecord]:
        data = self._repository.get_source_data(source=source)

        return [
            StudentRecord(
                student=model["student"],
                date=date.fromisoformat(model["date"]),
                coffee_spent=int(model["coffee_spent"]),
                sleep_hours=float(model["sleep_hours"]),
                study_hours=float(model["study_hours"]),
                mood=model["mood"],
                exam=model["exam"],
            )
            for model in data
        ]
