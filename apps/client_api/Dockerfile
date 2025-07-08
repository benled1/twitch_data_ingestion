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


COPY apps/client_api /app/client_api
WORKDIR /app/client_api
RUN uv pip install --system .

EXPOSE 8000
CMD ["uvicorn", "client_api.__main__:app", "--host", "0.0.0.0", "--port", "8000"]
