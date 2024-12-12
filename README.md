# AI Analytics Library

A modular Python library for AI analytics with deployable agents.

## Features

- Modular AI agents for different analytics tasks
- FastAPI integration for easy deployment
- Extensible architecture
- Built-in monitoring and logging
- Configurable through environment variables

## Installation

```bash
pip install ai-analytics
```

## Quick Start

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

## Documentation

For detailed documentation, visit the [docs](./docs) directory.

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

## License

MIT License