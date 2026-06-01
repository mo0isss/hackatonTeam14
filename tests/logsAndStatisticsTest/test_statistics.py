import json
import pytest
from src.logsAndStatistics.statistics import Statistics


@pytest.fixture
def statistics():
    return Statistics()


def test_default_values(statistics):
    assert statistics.files_count == 0
    assert statistics.processed_files == 0
    assert statistics.error_files == 0
    assert len(statistics.categories) == 0
    assert statistics.errors == []


def test_count_file(statistics):
    statistics.count_file()

    assert statistics.files_count == 1


def test_record_success(statistics):
    statistics.record_success("spam")
    statistics.record_success("spam")
    statistics.record_success("finance")

    assert statistics.processed_files == 3
    assert statistics.categories["spam"] == 2
    assert statistics.categories["finance"] == 1


def test_add_error(statistics):
    statistics.add_error("bad_file.txt", "file is broken")

    assert statistics.error_files == 1
    assert statistics.errors[0]["file"] == "bad_file.txt"
    assert statistics.errors[0]["error"] == "file is broken"


def test_create_statistics_report(statistics):
    statistics.count_file()
    statistics.record_success("spam")
    statistics.add_error("bad_file.txt", "file is broken")

    report = statistics.create_statistics()

    assert "Общее количество файлов: 1" in report
    assert "Обработано без ошибок: 1" in report
    assert "Количество ошибок: 1" in report
    assert "- spam: 1" in report
    assert "bad_file.txt" in report
    assert "file is broken" in report


def test_save_json(statistics, tmp_path):
    statistics.count_file()
    statistics.record_success("spam")

    json_path = tmp_path / "statistics.json"
    statistics.save_json(json_path)

    assert json_path.exists()

    with open(json_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    assert data["files_count"] == 1
    assert data["processed_files"] == 1
    assert data["error_files"] == 0
    assert data["categories"]["spam"] == 1


def test_save_txt(statistics, tmp_path):
    statistics.count_file()
    statistics.record_success("spam")

    txt_path = tmp_path / "statistics.txt"
    statistics.save_txt(txt_path)

    assert txt_path.exists()

    text = txt_path.read_text(encoding="utf-8")

    assert "Общее количество файлов: 1" in text
    assert "Обработано без ошибок: 1" in text
    assert "- spam: 1" in text