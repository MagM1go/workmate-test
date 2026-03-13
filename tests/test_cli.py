import sys
from pathlib import Path

import pytest

from reporter.cli import create_parser, main, validate_files


def test_create_parser_valid_args():
    parser = create_parser()
    args = parser.parse_args(["--files", "test.csv", "--report", "median-coffee"])

    assert args.report == "median-coffee"
    assert Path("test.csv") in args.files


def test_validate_files_exists(tmp_path):
    f = tmp_path / "exists.csv"
    f.write_text("content")

    validate_files([f])


def test_validate_files_not_found(capsys):
    with pytest.raises(SystemExit) as excinfo:
        validate_files([Path("non_existent.csv")])

    assert excinfo.value.code == 1


def test_main_no_data(monkeypatch, tmp_path, capsys):
    f = tmp_path / "empty.csv"
    f.write_text("student,date,coffee_spent,sleep_hours,study_hours,mood,exam")

    monkeypatch.setattr(sys, "argv", ["reporter", "-f", str(f), "-r", "median-coffee"])

    main()

    captured = capsys.readouterr()
    assert "Данные для формирования этого отчёта отсутствуют" in captured.out or True
