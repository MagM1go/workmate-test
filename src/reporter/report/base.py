from abc import ABC, abstractmethod

from reporter.chain.reader import StudentRecord

type ReportRow = dict[str, str | float]
type ReportResult = list[ReportRow]


class BaseReport(ABC):
    @abstractmethod
    def create(self, rows: list[StudentRecord]) -> ReportResult:
        """
        Генерирует отчёт на основе сырых строк из CSV.

        :param rows: список доменных записей StudentRecord
        :return: данные отчёта в виде списка словарей для последующего рендера
        """
