# hackatonTeam14
# Email Processing System

Автоматическая система обработки корпоративной почты. Читает письма из папки `inbox`, классифицирует их по категориям и раскладывает в соответствующие папки.


# Установка
git clone https://github.com/mo0isss/hackatonTeam14.git
cd hackatonTeam14

# Запуск
bash src/bash-script.sh

# Сруктура проекта
hackatonTeam14/
|- inbox/              # папка с входящими письмами (добавляется пользователем)
|- treated/            # папка с обработанными письмами (создаётся автоматически при вызове баш-скрипта)
|- src/
|   |-identifier/     # модуль классификации
|   |-logsAbndStatisctics #модуль логов и статистики
│   |- mover/          # модуль перемещения писем
│   |- parser/         # модуль парсинга писем
│   |-bash-script      # bash-скрипт для запуска
|- tests/              # тесты
|   |-identifierTest  # тесты для классификации 
|   |-logsAndStatisticsTest # тесты логов и статистики 
|   |-moverTest # тесты перемещения писем 
|   |-parserTest # тесты парсинга писем
|- main.py             # главный файл, слияющий все модули
|- conftest.py #без него не работают тесты у одного члена команды
|- requirements.txt    # зависимости
