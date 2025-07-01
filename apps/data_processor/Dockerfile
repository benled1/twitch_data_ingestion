FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential \
      curl \
      cron && \
    rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

COPY core /app/core
WORKDIR /app/core
RUN uv pip install --system .

COPY apps/data_processor /app/data_processor
WORKDIR /app/data_processor
RUN uv pip install --system .

COPY apps/data_processor/data_processor.cron /etc/cron.d/data_processor
RUN chmod 0644 /etc/cron.d/data_processor \
 && crontab /etc/cron.d/data_processor

RUN touch /var/log/data_processor.log

CMD ["cron", "-f"]
