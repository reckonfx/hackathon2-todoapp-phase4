# Quickstart Guide: Phase-2 Web-Based Todo Application

## Prerequisites

- Node.js 18+ (for frontend)
- Python 3.14+ (for backend)
- PostgreSQL 16+ (or access to Neon database)
- Docker and Docker Compose (optional, for containerized deployment)

## Environment Setup

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your database and auth configuration
   ```

5. Run database migrations:
   ```bash
   alembic upgrade head
   ```

6. Start the backend server:
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your backend API URL
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

## Database Configuration

The application uses PostgreSQL with Neon. Update your `.env` file in the backend with:

```env
DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
```

## API Documentation

The backend API documentation is automatically available at:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

## Running Tests

### Backend Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src
```

### Frontend Tests
```bash
# Run unit tests
npm run test

# Run E2E tests
npm run test:e2e
```

## Docker Deployment

For containerized deployment, use the provided docker-compose file:

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

## Default API Endpoints

- Backend API: http://localhost:8000/api/
- Frontend App: http://localhost:3000
- API Documentation: http://localhost:8000/docs