from abc import ABC, abstractmethod

from reporter.chain.reader import StudentRecord


class BaseReport(ABC):
    @abstractmethod
    def create(self, rows: list[StudentRecord]) -> list[dict[str, str | float]]:
        """
        Генерирует отчёт на основе сырых строк из CSV.

        :param rows: список строк, каждая — dict с ключами из заголовка CSV
        :return: сформированный отчёт в виде типа T
        """
