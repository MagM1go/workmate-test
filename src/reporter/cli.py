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
        choices=REPORT_CATEGORIES.keys(),
        help="Тип отчёта",
    )

    return parser


def validate_files(files: list[Path]) -> None:
    for file in files:
        if not file.is_file():
            logger.error(f"Файл не найден или недоступен: {file}")
            sys.exit(1)


def generate_report(
    files: list[Path], report_name: str
) -> list[dict[str, str | float]]:
    rows: list[StudentRecord] = []

    for file in files:
        reader = DataReader(get_repository_for_file(file))
        rows.extend(reader.read(file))

    if not rows:
        return []

    strategy = REPORT_CATEGORIES[report_name]()
    return strategy.create(rows)


def render_table(result: list[dict[str, str | float]]) -> str:
    return tabulate.tabulate(
        result,
        headers="keys",
        tablefmt="rounded_grid",
        numalign="right",
    )


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()

    validate_files(args.files)

    try:
        result = generate_report(args.files, args.report)
    except ValueError as e:
        logger.error(f"Ошибка данных: {e}")
        sys.exit(1)
    except OSError as e:
        logger.error(f"Ошибка чтения файла: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Непредвиденная ошибка: {e}")
        sys.exit(1)

    if not result:
        logger.warning("Недостаточно данных для формирования отчёта.")
        return

    print(render_table(result))


if __name__ == "__main__":
    main()
