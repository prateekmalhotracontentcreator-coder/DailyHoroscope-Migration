# ════════════════════════════════════════════════════════════
# PYTHON VERSION: 3.11 — LOCKED. DO NOT CHANGE WITHOUT TEAM SIGN-OFF.
#
# Why this is locked:
# flatlib (Vedic chart engine) depends on pyswisseph, a C extension.
# pyswisseph uses PyUnicode_AS_DATA which was removed in Python 3.12.
# Upgrading to 3.12 will break the Docker build with a C compile error.
# This affects Birth Chart, Kundali Milan, Brihat Kundli, and Panchang.
# Python 3.11 is supported until October 2027 — no urgency to change.
#
# To unblock 3.12: replace flatlib with a 3.12-compatible astronomy lib.
# That is a tracked future task, not a drop-in change.
# ════════════════════════════════════════════════════════════
FROM python:3.11-slim

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
