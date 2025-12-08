# Vocab Backend

FastAPI backend with PostgreSQL database.

## Setup

### With Poetry (Recommended)

```bash
# Install dependencies
poetry install

# Run development server
poetry run uvicorn main:app --reload

# Add new dependency
poetry add package-name

# Add dev dependency
poetry add --group dev package-name
```

### With Docker

```bash
# From root directory
docker-compose up backend
```

## Environment Variables

Create a `.env` file (see `.env.example`):

```env
POSTGRES_USER=vocab_user
POSTGRES_PASSWORD=vocab_password
POSTGRES_DB=vocab_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Project Structure

```
/backend
  /app
    /api/v1
      /endpoints     # API route handlers
      router.py      # Main API router
    /core
      config.py      # Settings & configuration
      database.py    # Database connection
      security.py    # Auth utilities
    /models          # SQLAlchemy models
  main.py            # FastAPI application
  pyproject.toml     # Poetry dependencies
  Dockerfile
```

## API Documentation

When running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
