# Используем легковесный Python
FROM python:3.11-slim

# Устанавливаем необходимые инструменты
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Рабочая директория
WORKDIR /app

# Копируем проект
COPY . .

# Устанавливаем зависимости через uv
RUN uv sync

# Открываем порт
EXPOSE 3002

# Запуск сервера
ENTRYPOINT ["sh", "-c", "uv run ncbi_mcp"]
