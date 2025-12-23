FROM python:3.11-slim

WORKDIR /app

# Install system dependencies in one layer and clean up
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry==2.2.1

# Configure Poetry to not create virtual environments (before installing)
RUN poetry config virtualenvs.create false

# Copy only dependency files first (better layer caching)
COPY pyproject.toml poetry.lock* ./

# Install dependencies (this layer will be cached if dependencies don't change)
RUN poetry install --no-interaction --no-ansi --no-root --only main

# Copy application code (changes here won't rebuild dependencies)
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
