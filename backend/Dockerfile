# ════════════════════════════════════════════════════════════
# PYTHON VERSION: 3.12
#
# Upgraded from 3.11 after completing the flatlib → pyswisseph migration.
# flatlib was the sole blocker (its C extension used PyUnicode_AS_DATA,
# removed in Python 3.12). flatlib has been replaced with direct pyswisseph
# calls in vedic_calculator.py. Python 3.12 is now the confirmed runtime.
#
# All Codex module deliveries (panchang_router, tarot_router,
# numerology_router, vedic_calculator) validated on Python 3.12.
# ════════════════════════════════════════════════════════════
FROM python:3.12-slim

WORKDIR /app

# Build tools required by pyswisseph C extension
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD uvicorn server:app --host 0.0.0.0 --port ${PORT:-8000}
