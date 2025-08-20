FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libgomp1 \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ .

# Create directories
RUN mkdir -p public && chmod 755 public

# Create non-root user
RUN adduser --disabled-password --gecos '' app \
    && chown -R app:app /app

# For port 80, we need to run as root or use a different port
# Let's use port 3000 internally and let CapRover handle the mapping
USER app

EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1

CMD ["gunicorn", "--config", "gunicorn.conf.py", "app:app"]