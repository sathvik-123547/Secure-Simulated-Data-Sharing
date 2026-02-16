# Base image for all services
FROM python:3.10-slim

WORKDIR /app

# System dependencies for crypto (gmpy2, etc if needed for py_ecc optimization)
# py_ecc is pure python so minimal deps needed.
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ src/
COPY pyproject.toml .

# Environment setup
ENV PYTHONPATH=/app
