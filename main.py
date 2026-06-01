from pathlib import Path
from src.parser.EmailParser import EmailParser
from src.identifier.classification import Classification
from src.mover.mover import mover
from src.logsAndStatistics.logger import (init_logger, log_start, log_processed_file, log_error, log_finish)
from src.logsAndStatistics.statistics import Statistics

def main():
    inbox_path = Path("inbox")
    logger = init_logger()
    statistics = Statistics()
    log_start(logger, inbox_path)

    if not inbox_path.exists():
        print("Error: there is no such folder in directory")
        log_error(logger, inbox_path, "there is no such folder in directory")
        log_finish(logger)
        statistics.save_json()
        statistics.save_txt()
        return
    
    parser = EmailParser()
    classifier = Classification()
    letters = list(inbox_path.glob("*"))

    if len(letters) == 0:
        print('Inbox folder is empty')
        log_error(logger, inbox_path, "Inbox folder is empty")
        log_finish(logger)
        statistics.save_json()
        statistics.save_txt()
        return
    
    for letter in letters:
        statistics.count_file()

        try:
            email = parser.parse(str(letter))
            category = classifier.classify(email)
            new_path = mover(str(letter), category)
            
            statistics.record_success(category)
            log_processed_file(logger, letter, category, new_path)

        except Exception as error:
            print(f"Error occurred: {letter.name}: {error}")
            statistics.add_error(letter, error)
            log_error(logger, letter, error)
            
            try:
                new_path = mover(str(letter), "other")
                log_processed_file(logger, letter, "other", new_path)
            except Exception as move_error:
                statistics.add_error(letter, move_error)
                log_error(logger, letter, move_error)

    log_finish(logger)

    statistics.print_statistics()
    statistics.save_json()
    statistics.save_txt()

if __name__ == "__main__":
    main()