# ════════════════════════════════════════════════════════════
# PYTHON VERSION: 3.12
#
# setuptools pinned explicitly: razorpay==1.3.0 imports pkg_resources at
# startup; python:3.12-slim ships without setuptools so we install it
# first in its own layer before the full requirements install.
# ════════════════════════════════════════════════════════════
FROM python:3.12-slim

WORKDIR /app

# Build tools required by pyswisseph C extension
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Pin setuptools before anything else so pkg_resources is available
# Note: version specifier must be quoted to avoid shell redirect interpretation
RUN pip install --no-cache-dir "setuptools>=68.0"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD uvicorn server:app --host 0.0.0.0 --port ${PORT:-8000}
