import pytest
from src.logsAndStatistics.logger import (init_logger, log_start, log_processed_file, log_error, log_finish)

@pytest.fixture
def log_path(tmp_path):
    return tmp_path / "test.log"


@pytest.fixture
def logger(tmp_path):
    return init_logger(log_folder=tmp_path, log_filename="test.log")


def test_log_file_is_created(log_path, logger):
    assert log_path.exists()
    assert logger.name == "mail_sorter"


def test_log_start(logger, log_path):
    log_start(logger, "inbox")
    text = log_path.read_text(encoding="utf-8")

    assert "Начата обработка папки: inbox" in text


def test_log_processed_file(logger, log_path):
    log_processed_file(
        logger,
        "inbox/mail_1.txt",
        "spam",
        "treated/spam/mail_1.txt"
    )

    text = log_path.read_text(encoding="utf-8")

    assert "Файл обработан: inbox/mail_1.txt" in text
    assert "Категория: spam" in text
    assert "Перемещен в: treated/spam/mail_1.txt" in text


def test_log_error(logger, log_path):
    log_error(logger, "bad_file.txt", "file is broken")
    text = log_path.read_text(encoding="utf-8")

    assert "Ошибка при обработке файла bad_file.txt: file is broken" in text


def test_log_finish(logger, log_path):
    log_finish(logger)
    text = log_path.read_text(encoding="utf-8")

    assert "Обработка почты завершена" in text