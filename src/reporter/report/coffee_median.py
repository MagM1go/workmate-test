import statistics
from collections import defaultdict
from typing import override

from reporter.chain.reader import StudentRecord
from reporter.report.base import BaseReport


class CoffeeMedianReport(BaseReport):
    @override
    def create(self, rows: list[StudentRecord]) -> list[dict[str, str | float]]:
        spending: defaultdict[str, list[int]] = defaultdict(list)

        for row in rows:
            spending[row.student].append(row.coffee_spent)

        result = [
            {"student": student, "coffee_spent": statistics.median(amounts)}
            for student, amounts in spending.items()
        ]

        return sorted(result, key=lambda r: r["coffee_spent"], reverse=True)
