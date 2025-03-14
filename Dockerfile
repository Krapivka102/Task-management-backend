# Промежуточный образ для сборки
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

# Устанавливаем необходимые пакеты для установки uv
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    gcc \
    python3-dev \
    libpq-dev \
    build-essential


# Копируем проект в образ
ADD . /opt/app

# Устанавливаем рабочую директорию
WORKDIR /opt/app

# Устанавливаем зависимости проекта
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-editable

# Синхронизируем проект
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-editable

# Финальный образ
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    vim \
    locales \
    tzdata \
    postgresql-client \
    && sed -i '/ru_RU.UTF-8/s/^# //g' /etc/locale.gen && locale-gen \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV LANG ru_RU:ru
ENV LANGUAGE ru_Ru:ru
ENV LC_ALL ru_RU.UTF-8

# Копируем виртуальную среду из промежуточного образа
COPY --from=builder /opt/app/.venv /opt/app/.venv

# Копируем проект в финальный образ
COPY --from=builder /opt/app /opt/app

# Устанавливаем рабочую директорию
WORKDIR /opt/app

EXPOSE 80

# Устанавливаем переменную окружения для использования виртуальной среды
ENV PATH="/opt/app/.venv/bin:$PATH"

VOLUME /static/
VOLUME /media/
VOLUME /logs/

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
