# Используем легковесный Python
FROM python:3.11-slim

# Устанавливаем необходимые инструменты
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем uv (если всё же нужен для других команд)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Рабочая директория
WORKDIR /app

# Копируем проект в контейнер
COPY . .

# Ставим пакет в editable mode (чтобы import mcp работал)
RUN pip install --no-cache-dir -e .

# На всякий случай добавим путь к проекту
ENV PYTHONPATH="/app:$PYTHONPATH"

# Открываем порт
EXPOSE 3002

# Запуск сервера
ENTRYPOINT ["python", "ncbi_mcp_server/server.py"]
