FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:${PATH}"

COPY core /app/core
RUN uv pip install --system ./core

COPY apps/data_ingestor /app/data_ingestor
WORKDIR /app/data_ingestor
RUN uv pip install --system .

CMD ["python", "-m", "data_ingestor", "--channel_limit", "20"]
