FROM python:3.12-slim AS builder

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

RUN apt-get update && apt-get upgrade -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 appuser

COPY --from=builder /root/.local /home/appuser/.local

COPY alembic.ini .
COPY src/ ./src
COPY infrastructure/ ./infrastructure

RUN chown -R appuser:appuser /app /home/appuser/.local

USER appuser

ENV PATH=/home/appuser/.local/bin:$PATH