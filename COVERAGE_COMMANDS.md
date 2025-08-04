# 📊 Команды для тестового покрытия (Coverage)

## 🚀 Быстрый старт

### Установка зависимостей
```bash
pip install pytest-cov coverage
```

### Запуск coverage
```bash
# Простой запуск
python run_coverage.py

# Или напрямую через pytest
pytest test_*.py --cov=. --cov-report=term-missing --cov-report=html:htmlcov -v
```

## 📈 Команды для анализа покрытия

### Базовые команды
```bash
# Запуск тестов с покрытием
pytest test_*.py --cov=. -v

# Подробный отчет с пропущенными строками
pytest test_*.py --cov=. --cov-report=term-missing -v

# HTML отчет
pytest test_*.py --cov=. --cov-report=html:htmlcov -v

# XML отчет (для CI/CD)
pytest test_*.py --cov=. --cov-report=xml -v

# Все форматы отчетов
pytest test_*.py --cov=. --cov-report=term-missing --cov-report=html:htmlcov --cov-report=xml -v
```

### Анализ конкретных файлов
```bash
# Покрытие только основных файлов
pytest test_*.py --cov=main --cov=models --cov=schemas --cov=utils -v

# Исключение тестовых файлов
pytest test_*.py --cov=. --cov-report=term-missing --omit="test_*.py" -v
```

### Детальный анализ
```bash
# Показать статистику coverage
coverage report --show-missing

# Показать пропущенные строки
coverage report -m

# Создать HTML отчет
coverage html

# Показать детали по файлу
coverage report --include="main.py"
```

## 🎯 Целевые показатели покрытия

### Хорошее покрытие:
- **90%+** - Отличное покрытие
- **80-90%** - Хорошее покрытие
- **70-80%** - Приемлемое покрытие
- **<70%** - Требует улучшения

### Файлы для особого внимания:
- `main.py` - основные эндпоинты API
- `models.py` - модели базы данных
- `schemas.py` - валидация данных
- `utils.py` - бизнес-логика

## 📊 Интерпретация отчетов

### В терминале:
```
Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
main.py                    45      2    96%   15, 23
models.py                  30      0   100%
schemas.py                 25      1    96%   12
utils.py                   20      3    85%   8-10
-----------------------------------------------------
TOTAL                     120      6    95%
```

### В HTML отчете:
- **Зеленые строки** - выполнены
- **Красные строки** - пропущены
- **Желтые строки** - частично выполнены

## 🔧 Настройка .coveragerc

Файл `.coveragerc` содержит:
- **omit** - файлы для исключения
- **exclude_lines** - строки для исключения
- **source** - директории для анализа

## 🚀 Интеграция с CI/CD

### GitHub Actions пример:
```yaml
- name: Run tests with coverage
  run: |
    pytest test_*.py --cov=. --cov-report=xml --cov-report=term-missing
    coverage report --fail-under=80
```

### GitLab CI пример:
```yaml
test:
  script:
    - pytest test_*.py --cov=. --cov-report=xml
    - coverage report --fail-under=80
```

## 💡 Советы по улучшению покрытия

### 1. Добавьте тесты для:
- Обработки ошибок
- Граничных случаев
- Валидации данных
- Исключительных ситуаций

### 2. Исключите из покрытия:
- Тестовые файлы
- Скрипты утилит
- Миграции базы данных
- Конфигурационные файлы

### 3. Фокус на:
- Основную бизнес-логику
- API эндпоинты
- Модели данных
- Валидацию

## 📈 Мониторинг прогресса

### Еженедельная проверка:
```bash
# Запуск полного анализа
python run_coverage.py

# Сравнение с предыдущим отчетом
coverage diff
```

### Целевые показатели:
- **main.py**: 95%+
- **models.py**: 100%
- **schemas.py**: 95%+
- **utils.py**: 90%+
- **Общее покрытие**: 90%+ 