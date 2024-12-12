# AI Analytics Library

A modular Python library for AI analytics with deployable agents.

## Features

- Modular AI agents for different analytics tasks
- Natural language to SQL translation
- Multiple database support (PostgreSQL, BigQuery)
- FastAPI integration for easy deployment
- Extensible architecture
- Built-in monitoring and logging
- Configurable through environment variables

## Installation

```bash
pip install ai-analytics
```

## Quick Start

### Text Analysis

```python
from ai_analytics import TextAnalysisAgent
from ai_analytics.config import Settings

# Initialize settings
settings = Settings()

# Create an agent
agent = TextAnalysisAgent(settings)

# Analyze text
result = agent.analyze("Your text here")
print(result)
```

### SQL Chat

```python
from ai_analytics import SQLChatAgent, SQLChatRequest
from ai_analytics.config import Settings
from ai_analytics.database import PostgresConnection

# Initialize database connection
db = PostgresConnection(
    host="localhost",
    database="your_db",
    user="user",
    password="password",
    table="your_table"
)

# Initialize agent
settings = Settings(openai_api_key="your-key")
agent = SQLChatAgent(settings, database=db)

# Ask a question
request = SQLChatRequest(
    question="What were the top 5 sales by revenue last month?",
    context="We're interested in completed sales only"
)

# Get results
response = await agent.execute(request)
print(f"SQL Query: {response['generated_sql']}")
print(f"Results: {response['results']}")

# Get suggested questions
questions = await agent.suggest_questions()
print("Suggested questions:", questions)
```

## SQL Chat API

The library includes a FastAPI application for deploying SQL Chat functionality as a web service.

### Running the API

1. Copy and configure the environment file:
```bash
cd examples
cp .env.example .env
# Edit .env with your credentials
```

2. Install dependencies:
```bash
pip install ".[dev]"
pip install python-dotenv httpx
```

3. Start the API server:
```bash
uvicorn sql_chat_api:app --reload
```

4. Test the API:
```bash
python test_sql_chat_api.py
```

### API Endpoints

The API provides the following endpoints:

- `POST /query`: Execute natural language queries
- `GET /schema`: Get database schema and sample data
- `GET /suggest-questions`: Get AI-generated question suggestions
- `GET /health`: Health check endpoint

API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Example API Usage

Using curl:
```bash
# Get schema
curl -X GET "http://localhost:8000/schema" \
     -H "Content-Type: application/json" \
     -d '{"db_type": "postgres", ...}'

# Execute query
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"question": "What are the top sales?", ...}'
```

## Development

1. Clone the repository
2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
3. Run tests:
   ```bash
   pytest
   ```

## Running with Docker

The examples directory includes a complete setup for running both the backend API and frontend UI using Docker Compose.

### Prerequisites

- Docker and Docker Compose installed
- OpenAI API key

### Quick Start

1. Navigate to the examples directory:
   ```bash
   cd examples
   ```

2. Copy the environment file and edit with your settings:
   ```bash
   cp .env.docker .env
   # Edit .env with your OpenAI API key and other settings
   ```

3. Run the application:
   ```bash
   ./run-docker.sh
   ```

4. Access the application:
   - Frontend UI: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Docker Services

The Docker setup includes:

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

### Development with Docker

- Changes to the code will automatically reload both services
- Backend logs and frontend development server output are visible in the Docker Compose output
- Use `docker-compose logs -f [service]` to follow specific service logs
- Use `docker-compose down` to stop all services

## Project Structure

```
ai_analytics_lib/
├── src/
│   └── ai_analytics/
│       ├── agents/
│       │   ├── base.py
│       │   ├── text_analysis.py
│       │   └── sql_chat.py
│       ├── database/
│       │   ├── base.py
│       │   ├── postgres.py
│       │   └── bigquery.py
│       └── utils/
│           └── logging.py
├── examples/
│   ├── sql_chat_api.py
│   └── test_sql_chat_api.py
└── tests/
```

## License

MIT License