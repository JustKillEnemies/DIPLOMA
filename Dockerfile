# 1. Берем полный образ Python 3.14 (со всеми инструментами сборки)
FROM python:3.14

# 2. Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# 3. Настройки, чтобы Python не тормозил и сразу выводил логи в консоль Докера
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 4. Сначала копируем только файл зависимостей, чтобы Докер кэшировал их
COPY pyproject.toml ./

# 5. Обновляем pip и ставим зависимости (используем poetry, так как он у тебя был)
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

# 6. Копируем твою папку с кодом
COPY src/ ./src/
ENV PYTHONPATH=/app

# 7. Открываем порт 8000 для внешнего мира
EXPOSE 8000

# 8. Команда запуска твоего сервиса
CMD ["python", "src/cli.py"]