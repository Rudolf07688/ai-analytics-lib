"""
A simple example demonstrating the core AI Analytics library functionality.
"""
import asyncio
from ai_analytics import SQLChatAgent, SQLChatRequest
from ai_analytics.config import Settings
from ai_analytics.database import PostgresConnection

async def main():
    # Initialize database connection
    db = PostgresConnection(
        host="localhost",
        database="example_db",
        user="user",
        password="password",
        table="sales"
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