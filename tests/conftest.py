from datetime import date

import pytest

from reporter.chain.reader import StudentRecord


@pytest.fixture
def csv_rows() -> list[dict[str, str]]:
    return [
        {
            "student": "биба",
            "date": "2222-02-22",
            "coffee_spent": "2",
            "sleep_hours": "7.5",
            "study_hours": "4",
            "mood": "труп",
            "exam": "физика",
        },
        {
            "student": "боба",
            "date": "2222-02-22",
            "coffee_spent": "5",
            "sleep_hours": "5.0",
            "study_hours": "8",
            "mood": "отл",
            "exam": "физика",
        },
        {
            "student": "биба",
            "date": "2222-02-23",
            "coffee_spent": "4",
            "sleep_hours": "6.5",
            "study_hours": "5",
            "mood": "норм",
            "exam": "физика",
        },
    ]


@pytest.fixture
def student_records() -> list[StudentRecord]:
    return [
        StudentRecord("биба", date(2222, 2, 22), 2, 7.5, 4.0, "труп", "физика"),
        StudentRecord("боба", date(2222, 2, 22), 5, 5.0, 8.0, "отл", "физика"),
        StudentRecord("биба", date(2222, 2, 23), 4, 6.5, 5.0, "норм", "физика"),
    ]
