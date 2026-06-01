import logging
from pathlib import Path
from datetime import datetime

def init_logger(log_folder="logs", log_filename=None):
    log_folder = Path(log_folder)
    log_folder.mkdir(parents=True, exist_ok=True)

    if log_filename is None:
        timetamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_filename = f"mail_sorter_{timetamp}.log"

    log_path = log_folder/log_filename
    logger = logging.getLogger("mail_sorter")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)

    console_output = logging.StreamHandler()
    console_output.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_output)

    logger.info("Логирование запущено")
    logger.info(f"Файл лога: {log_path}")
    return logger

def log_start(logger, inbox_path):
    logger.info(f"Начата обработка папки: {inbox_path}")

def log_processed_file(logger, file_path, category, new_path):
    logger.info(
        f"Файл обработан: {file_path} | "
        f"Категория: {category} | "
        f"Перемещен в: {new_path}"
    )

def log_error(logger, file_path, error):
    logger.error(f"Ошибка при обработке файла {file_path}: {error}")

def log_finish(logger):
    logger.info("Обработка почты завершена")