FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install poetry
RUN pip install --no-cache-dir poetry

# Copy dependency files
COPY ../pyproject.toml ../poetry.lock* ./

# Install dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

# Copy necessary files from parent directory
COPY ../.env* ./
COPY ../icloud_session.pkl ./
COPY ../account.json ./
COPY ../ani_libs.bin ./

# Copy the application
COPY app.py ./track_location/

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/')" || exit 1

# Run the application
CMD ["python", "track_location/app.py"]
