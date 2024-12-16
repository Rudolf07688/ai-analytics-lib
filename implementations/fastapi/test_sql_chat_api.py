"""Test script for SQL Chat API."""

import asyncio
import os
from dotenv import load_dotenv
import httpx

# Load environment variables
load_dotenv()

# API base URL
BASE_URL = "http://localhost:8000"

# PostgreSQL configuration
postgres_config = {
    "db_type": "postgres",
    "host": os.getenv("POSTGRES_HOST"),
    "port": int(os.getenv("POSTGRES_PORT", "5432")),
    "database": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "schema": os.getenv("POSTGRES_SCHEMA", "public"),
    "table": os.getenv("POSTGRES_TABLE"),
}


async def test_api():
    """Test the SQL Chat API endpoints."""
    async with httpx.AsyncClient() as client:
        # Test health check
        response = await client.get(f"{BASE_URL}/health")
        print("Health check:", response.json())

        # Set database configuration
        headers = {"Content-Type": "application/json"}
        
        # Get schema
        response = await client.get(
            f"{BASE_URL}/schema",
            json=postgres_config,
            headers=headers
        )
        print("\nSchema:", response.json())

        # Get suggested questions
        response = await client.get(
            f"{BASE_URL}/suggest-questions",
            json=postgres_config,
            headers=headers
        )
        print("\nSuggested questions:", response.json())

        # Execute a query
        query_request = {
            "question": "What are the top 5 records in the table?",
            "max_results": 5
        }
        response = await client.post(
            f"{BASE_URL}/query",
            json={**postgres_config, **query_request},
            headers=headers
        )
        result = response.json()
        print("\nQuery results:")
        print("SQL:", result["generated_sql"])
        print("Results:", result["results"])
        print(f"Execution time: {result['execution_time']:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(test_api())