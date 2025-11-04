# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Copy project files
COPY pyproject.toml poetry.lock* /app/

# Install Python dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

# Copy application code
COPY track_location/track_to_mongodb_docker.py /app/track_to_mongodb.py
COPY icloud_session.pkl /app/

# Environment variables (can be overridden by docker-compose or -e flag)
ENV TRACKING_INTERVAL=300
ENV PYTHONUNBUFFERED=1

# Run the tracking script in continuous mode
CMD ["python", "track_to_mongodb.py"]
