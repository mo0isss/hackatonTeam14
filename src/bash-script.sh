#!/bin/bash
echo "Анализ почтового ящика"
if [ ! -d "inbox" ]; then
    echo "Ошибка, папка 'inbox' не существует"
    exit 1
fi
file_count=$(find inbox -type f -name "*.eml" 2>/dev/null | wc -l)
echo "Найдено .eml файлов: $file_count"
echo "Анализ начался"
python3 main.py
exit_code=$?
echo "Анализ окончен"
if [ $exit_code -eq 0 ]; then
    echo "окончен успешно"
else
    echo "ошибка (код: $exit_code)"
fi
exit $exit_code