# pyright: reportUnusedCallResult=false, reportAny=false
import argparse
import logging
import sys
from pathlib import Path

import tabulate

from reporter.chain.reader import DataReader, StudentRecord
from reporter.chain.repository.base import BaseRepository
from reporter.chain.repository.csv_repository import CSVRepository
from reporter.report.base import BaseReport
from reporter.report.coffee_median import CoffeeMedianReport

# Решил сделать чуть расширяемее, если вдруг надо будет добавить новые типы данных
REPOSITORY_MAP: dict[str, type[BaseRepository]] = {
    ".csv": CSVRepository,
    # ".json": JSONRepository,
    # ...
}
REPORT_CATEGORIES: dict[str, type[BaseReport]] = {"median-coffee": CoffeeMedianReport}

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def get_repository_for_file(path: Path) -> BaseRepository:
    extension = path.suffix.lower()
    repository_cls: type[BaseRepository] | None = REPOSITORY_MAP.get(extension)

    if not repository_cls:
        available = ", ".join(REPOSITORY_MAP)
        raise ValueError(f"Формат {extension} не поддерживается. Доступно: {available}")

    return repository_cls()


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="reporter",
        usage="%(prog)s --files math.csv --report median-coffee",
        description="Программа для генерации отчетов о потреблении кофе студентами.",
    )

    parser.add_argument(
        "--files",
        "-f",
        nargs="+",
        type=Path,
        required=True,
        help="Пути к одному или нескольким CSV файлам для обработки",
    )

    parser.add_argument(
        "--report",
        "-r",
        type=str,
        required=True,
        choices=REPORT_CATEGORIES.keys(),  # Авто-валидация и подсказки в --help
        help="Название отчёта (можно указать несколько через пробел)",
    )

    return parser


def validate_files(files: list[Path]) -> None:
    for file in files:
        if not file.is_file():
            logger.error(f"Файл не найден или недоступен: {file}")
            sys.exit(1)


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()

    validate_files(args.files)

    rows: list[StudentRecord] = []

    try:
        for file in args.files:
            reader = DataReader(get_repository_for_file(file))
            rows.extend(reader.read(file))
    except Exception as e:
        logger.error(f"Критическая ошибка при чтении данных: {e}")
        sys.exit(1)

    if not rows:
        logger.warning("Файлы пусты или не содержат валидных данных.")
        return

    for report_name in args.report:
        strategy = REPORT_CATEGORIES[report_name]()
        result = strategy.create(rows)

        if not result:
            print("Данные для формирования этого отчёта отсутствуют.")
            continue

        print(
            tabulate.tabulate(
                result, headers="keys", tablefmt="rounded_grid", numalign="right"
            )
        )


if __name__ == "__main__":
    main()
