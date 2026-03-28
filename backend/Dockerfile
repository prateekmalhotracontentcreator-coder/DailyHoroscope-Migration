FROM python:3.12.9-slim

WORKDIR /app

# Build tools required by pyswisseph C extension
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    build-essential \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# setuptools must be installed explicitly: razorpay==1.3.0 imports
# pkg_resources at startup and python:3.12-slim omits setuptools.
RUN pip install --no-cache-dir "setuptools>=68.0"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD uvicorn server:app --host 0.0.0.0 --port ${PORT:-8000}
