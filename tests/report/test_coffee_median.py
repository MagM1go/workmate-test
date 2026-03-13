from reporter.report.coffee_median import CoffeeMedianReport


def test_coffee_median_report(student_records):
    report = CoffeeMedianReport()
    result = report.create(student_records)

    assert len(result) == 2

    assert result[0] == {"student": "боба", "coffee_spent": 5.0}
    assert result[1] == {"student": "биба", "coffee_spent": 3.0}
