from collections import Counter
from pathlib import Path
import json

class Statistics:
    def __init__(self):
        self.files_count = 0
        self.processed_files = 0
        self.error_files = 0
        self.categories = Counter()
        self.errors = []

    def count_file(self):
        self.files_count += 1

    def record_success(self, category):
        self.processed_files += 1
        self.categories[category] += 1

    def add_error(self, file_path, error):
        self.error_files += 1
        self.errors.append({"file": str(file_path), "error": str(error)})

    def to_dict(self):
        return {"files_count": self.files_count,
                "processed_files": self.processed_files,
                "error_files": self.error_files,
                "categories": dict(self.categories),
                "errors": self.errors
        }
    
    def create_statistics(self):
        lines=[]
        lines.append("~~ Статистика обработки почты ~~")
        lines.append(f"Общее количество файлов: {self.files_count}")
        lines.append(f"Обработано без ошибок: {self.processed_files}")
        lines.append(f"Количество ошибок: {self.error_files}")
        lines.append("")
        lines.append("Количество писем по категориям:")

        if self.categories:
            for category, count in self.categories.items():
                lines.append(f"- {category}: {count}")
        else:
            lines.append("- категорий пока нет")

        if self.errors:
            lines.append("")
            lines.append("Ошибки:")
            for error in self.errors:
                lines.append(f"- {error['file']}: {error['error']}")
        return "\n".join(lines)
    
    def print_statistics(self):
        print(self.create_statistics())

    def save_json(self, file_path="logs/statistics.json"):
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(self.to_dict(), file, ensure_ascii=False, indent=4)

    def save_txt(self, file_path="logs/statistics.txt"):
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(self.create_statistics())