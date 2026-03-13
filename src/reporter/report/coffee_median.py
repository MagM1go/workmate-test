import statistics
from collections import defaultdict
from typing import override

from reporter.chain.reader import StudentRecord
from reporter.report.base import BaseReport, ReportResult


class CoffeeMedianReport(BaseReport):
    @override
    def create(self, rows: list[StudentRecord]) -> ReportResult:
        spending: defaultdict[str, list[int]] = defaultdict(list)

        for row in rows:
            spending[row.student].append(row.coffee_spent)

        result = [
            {"student": student, "coffee_spent": float(statistics.median(amounts))}
            for student, amounts in spending.items()
        ]

        return sorted(result, key=lambda r: r["coffee_spent"], reverse=True)
