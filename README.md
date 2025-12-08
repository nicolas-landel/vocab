# Vocab App

A vocabulary learning application built with Vue 3, FastAPI, and PostgreSQL.

## Architecture

- **Frontend**: Vue 3 + Vite + Vue Router + Pinia
- **Backend**: FastAPI + SQLAlchemy + PostgreSQL
- **Deployment**: Docker + Docker Compose
- **Package Management**: Poetry (backend), pnpm (frontend)

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js 20+ and pnpm (for local frontend development)
- Python 3.11+ and Poetry (for local backend development)

### Development with Docker

1. **Clone and setup**
   ```bash
   cp .env.example .env
   ```

2. **Start all services**
   ```bash
   docker-compose up
   ```

   This will start:
   - PostgreSQL on `localhost:5432`
   - FastAPI backend on `localhost:8000`
   - Vue frontend on `localhost:5173`

3. **Access the app**
   - Frontend: http://localhost:5173
   - API docs: http://localhost:8000/docs
   - API health: http://localhost:8000/health

### Local Development (without Docker)

**Backend:**
```bash
cd backend
poetry install
poetry run uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
pnpm install
pnpm dev
```

**Database:**
You'll need PostgreSQL running locally or use Docker for just the database:
```bash
docker-compose up db
```

## Project Structure

```
/vocab
  /backend
    /app
      /api/v1/endpoints    # API endpoints
      /core               # Config, security, database
      /models            # SQLAlchemy models
    main.py             # FastAPI app
    pyproject.toml      # Poetry dependencies
    poetry.lock         # Locked dependencies
    Dockerfile
  /frontend             # Vue 3 app
    /src
      /api             # API client
      /components      # Vue components
      /router          # Vue Router
      /stores          # Pinia stores
      /views           # Page components
    index.html
    package.json
    vite.config.js
  docker-compose.yml
  README.md
```

## API Endpoints

- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login (returns JWT)
- `GET /api/v1/auth/me` - Get current user

## Environment Variables

See `.env.example` for all configuration options.
