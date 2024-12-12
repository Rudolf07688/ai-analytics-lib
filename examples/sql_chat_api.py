"""FastAPI example for SQL Chat functionality."""

import os
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from ai_analytics.agents import SQLChatAgent, SQLChatRequest, SQLChatResponse
from ai_analytics.config import Settings
from ai_analytics.database import BigQueryConnection, PostgresConnection


app = FastAPI(
    title="SQL Chat API",
    description="API for natural language queries to databases",
    version="0.1.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DatabaseConfig(BaseModel):
    """Database configuration model."""
    
    db_type: str = Field(..., description="Type of database (postgres or bigquery)")
    
    # PostgreSQL settings
    host: Optional[str] = None
    port: Optional[int] = 5432
    database: Optional[str] = None
    user: Optional[str] = None
    password: Optional[str] = None
    schema: Optional[str] = "public"
    table: Optional[str] = None
    
    # BigQuery settings
    project_id: Optional[str] = None
    dataset_id: Optional[str] = None
    table_id: Optional[str] = None
    credentials_json: Optional[str] = None


# Store database connections (in production, use proper connection management)
db_connections = {}


def get_settings() -> Settings:
    """Get application settings."""
    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4"),
    )


def get_agent(db_config: DatabaseConfig = Depends()) -> SQLChatAgent:
    """Get or create SQL Chat Agent for the specified database."""
    db_key = f"{db_config.db_type}:{db_config.database or db_config.project_id}"
    
    if db_key not in db_connections:
        if db_config.db_type == "postgres":
            if not all([db_config.host, db_config.database, db_config.user, db_config.password]):
                raise HTTPException(400, "Missing PostgreSQL connection details")
                
            db = PostgresConnection(
                host=db_config.host,
                port=db_config.port,
                database=db_config.database,
                user=db_config.user,
                password=db_config.password,
                schema=db_config.schema,
                table=db_config.table
            )
        elif db_config.db_type == "bigquery":
            if not all([db_config.project_id, db_config.dataset_id, db_config.table_id]):
                raise HTTPException(400, "Missing BigQuery connection details")
                
            db = BigQueryConnection(
                project_id=db_config.project_id,
                dataset_id=db_config.dataset_id,
                table_id=db_config.table_id,
                credentials_json=db_config.credentials_json
            )
        else:
            raise HTTPException(400, f"Unsupported database type: {db_config.db_type}")
            
        try:
            db.connect()
            agent = SQLChatAgent(get_settings(), database=db)
            db_connections[db_key] = agent
        except Exception as e:
            raise HTTPException(500, f"Failed to connect to database: {str(e)}")
    
    return db_connections[db_key]


@app.post("/query", response_model=SQLChatResponse)
async def query_database(
    request: SQLChatRequest,
    agent: SQLChatAgent = Depends(get_agent)
):
    """Execute a natural language query against the database."""
    try:
        result = await agent.execute(request)
        return result
    except Exception as e:
        raise HTTPException(500, f"Query execution failed: {str(e)}")


@app.get("/schema")
async def get_schema(agent: SQLChatAgent = Depends(get_agent)):
    """Get database schema and sample data."""
    try:
        return await agent.get_schema_overview()
    except Exception as e:
        raise HTTPException(500, f"Failed to get schema: {str(e)}")


@app.get("/suggest-questions", response_model=List[str])
async def suggest_questions(
    n: int = 3,
    agent: SQLChatAgent = Depends(get_agent)
):
    """Get suggested questions based on the schema."""
    try:
        return await agent.suggest_questions(n)
    except Exception as e:
        raise HTTPException(500, f"Failed to generate questions: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "0.1.0"}