# AI Analytics Library

A modular Python library for AI analytics with deployable agents and reference implementations.

## Project Structure

```plaintext
ai_analytics_lib/
├── src/ai_analytics/        # Core library
│   ├── agents/             # AI agents (SQL Chat, Text Analysis)
│   ├── database/           # Database adapters
│   └── utils/              # Utilities
├── implementations/        # Full-stack implementations
│   ├── fastapi/           # FastAPI + React implementation
│   └── rails/             # Ruby on Rails implementation
└── examples/              # Simple usage examples
```

## Features

- Modular AI agents for different analytics tasks
- Natural language to SQL translation
- Multiple database support (PostgreSQL, BigQuery)
- Multiple reference implementations:
  - FastAPI + React (Python)
  - Ruby on Rails
- Extensible architecture
- Built-in monitoring and logging
- Configurable through environment variables

## Installation

```bash
pip install ai-analytics
```

See the [Quick Start](#quick-start) section below for basic usage examples.

For full-stack implementations, see:
- [FastAPI Implementation](implementations/fastapi/README.md)
- [Rails Implementation](implementations/rails/README.md)

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
import asyncio
from ai_analytics import SQLChatAgent, SQLChatRequest
from ai_analytics.config import Settings
from ai_analytics.database import PostgresConnection

async def main():
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

if __name__ == "__main__":
    asyncio.run(main())
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

## Reference Implementations

The library includes two complete reference implementations:

### FastAPI + React Implementation

A modern Python-based implementation using FastAPI for the backend and React for the frontend. See [FastAPI Implementation](implementations/fastapi/README.md) for details.

Features:
- FastAPI backend with async support
- React frontend with TypeScript
- Docker Compose setup
- Hot reload for development
- Interactive API documentation

### Ruby on Rails Implementation

A traditional Ruby on Rails implementation with integrated frontend. See [Rails Implementation](implementations/rails/README.md) for details.

Features:
- Full Ruby on Rails stack
- Integrated frontend
- Docker support
- Production-ready configuration
- ActiveRecord database integration

## License

MIT License