import logging
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


def test_main_no_data(monkeypatch, tmp_path, caplog):
    f = tmp_path / "empty.csv"
    f.write_text("student,date,coffee_spent,sleep_hours,study_hours,mood,exam")

    monkeypatch.setattr(sys, "argv", ["reporter", "-f", str(f), "-r", "median-coffee"])

    with caplog.at_level(logging.WARNING):
        main()

    assert "Недостаточно данных для формирования отчёта." in caplog.text


def test_main_success(monkeypatch, tmp_path, capsys):
    f = tmp_path / "data.csv"
    f.write_text(
        "student,date,coffee_spent,sleep_hours,study_hours,mood,exam\n"
        "абоба,2024-06-01,100,7,5,труп,физика\n"
        "филя,2024-06-02,200,7,5,норм,физика\n"
        "нима,2024-06-01,300,6,8,отл,физика\n",
        encoding="utf8",
    )

    monkeypatch.setattr(
        sys,
        "argv",
        ["reporter", "--files", str(f), "--report", "median-coffee"],
    )

    main()
    captured = capsys.readouterr()

    assert "абоба" in captured.out
    assert "филя" in captured.out
    assert "coffee_spent" in captured.out


def test_create_parser_invalid_report():
    parser = create_parser()

    with pytest.raises(SystemExit):
        parser.parse_args(["--files", "test.csv", "--report", "unknown-report"])
