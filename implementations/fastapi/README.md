# FastAPI SQL Chat Implementation

A modern implementation of the AI Analytics SQL Chat using FastAPI and React.

## Features

- FastAPI backend with async support
- React frontend with TypeScript
- Docker Compose setup
- Hot reload for development
- Interactive API documentation

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- OpenAI API key

### Running with Docker

1. Copy the environment file and edit with your settings:
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key and other settings
   ```

2. Run the application:
   ```bash
   ./run-docker.sh
   ```

3. Access the application:
   - Frontend UI: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Manual Setup

1. Install backend dependencies:
   ```bash
   pip install -e ".[dev]"
   pip install python-dotenv httpx
   ```

2. Install frontend dependencies:
   ```bash
   cd sql-chat-frontend
   npm install
   ```

3. Start the backend:
   ```bash
   uvicorn sql_chat_api:app --reload
   ```

4. Start the frontend:
   ```bash
   cd sql-chat-frontend
   npm run dev
   ```

## API Endpoints

- `POST /query`: Execute natural language queries
- `GET /schema`: Get database schema and sample data
- `GET /suggest-questions`: Get AI-generated question suggestions
- `GET /health`: Health check endpoint

## Development

- Backend code is in `sql_chat_api.py`
- Frontend code is in the `sql-chat-frontend` directory
- Tests are in `test_sql_chat_api.py`

### Docker Services

1. Backend Service:
   - FastAPI application
   - Automatic code reloading
   - Volume mounted for development
   - Exposed on port 8000

2. Frontend Service:
   - React application with Vite
   - Hot module replacement
   - Volume mounted for development
   - Exposed on port 3000

### Development Tips

- Changes to the code will automatically reload both services
- Backend logs and frontend development server output are visible in the Docker Compose output
- Use `docker-compose logs -f [service]` to follow specific service logs
- Use `docker-compose down` to stop all services