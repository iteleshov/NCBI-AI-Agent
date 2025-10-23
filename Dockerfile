# Берём легковесный Python
FROM python:3.11-slim

# Устанавливаем необходимые инструменты
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Копируем проект
COPY . .

# Устанавливаем зависимости через pip
RUN pip install --upgrade pip
RUN pip install -e .

# Открываем порт (меняй под свой uv сервер)
EXPOSE 3002

# Запуск сервера
ENTRYPOINT ["python", "-m", "ncbi_mcp_server"]
