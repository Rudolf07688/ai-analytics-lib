"""SQL Chat Agent implementation."""

from typing import Any, Dict, List, Optional, Union
import json

import openai
from pydantic import BaseModel, Field

from ai_analytics.agents.base import BaseAgent
from ai_analytics.database import DatabaseConnection, BigQueryConnection, PostgresConnection
from ai_analytics.database.base import TableSchema


class SQLChatRequest(BaseModel):
    """Request model for SQL chat interactions."""
    
    question: str = Field(..., description="Natural language question about the data")
    context: Optional[str] = Field(None, description="Additional context for the question")
    max_results: int = Field(100, description="Maximum number of results to return")


class SQLChatResponse(BaseModel):
    """Response model for SQL chat interactions."""
    
    question: str
    generated_sql: str
    results: List[Dict[str, Any]]
    column_names: List[str]
    execution_time: float
    row_count: int


class SQLChatAgent(BaseAgent):
    """Agent for natural language to SQL interactions."""

    def __init__(self, settings: Any, database: DatabaseConnection):
        """Initialize SQL Chat Agent.
        
        Args:
            settings: Configuration settings
            database: Database connection instance
        """
        super().__init__(settings)
        self.database = database
        self.schema: Optional[TableSchema] = None

    def _validate_settings(self) -> None:
        """Validate required settings."""
        if not self.settings.openai_api_key:
            raise ValueError("OpenAI API key is required")

    def _initialize_client(self) -> None:
        """Initialize OpenAI client."""
        openai.api_key = self.settings.openai_api_key
        # Cache the schema for future use
        self.schema = self.database.get_schema()

    def _build_system_prompt(self) -> str:
        """Build system prompt for SQL generation.
        
        Returns:
            Formatted system prompt string
        """
        schema_str = json.dumps(self.schema.dict(), indent=2)
        
        return f"""You are a SQL expert that helps translate natural language questions into SQL queries.
Given the following database schema:

{schema_str}

Your task is to:
1. Generate a valid SQL query that answers the user's question
2. Only use the tables and columns defined in the schema
3. Return ONLY the SQL query without any explanation
4. Use appropriate SQL functions and joins as needed
5. Ensure the query is optimized and follows best practices
6. Limit results as specified in the request

The database type is: {self.database.__class__.__name__}"""

    async def _process(self, input_data: SQLChatRequest) -> Dict[str, Any]:
        """Process natural language query and return results.
        
        Args:
            input_data: SQLChatRequest containing the question
            
        Returns:
            Dict containing query results and metadata
        """
        import time
        start_time = time.time()

        # Generate SQL query
        messages = [
            {"role": "system", "content": self._build_system_prompt()},
            {"role": "user", "content": input_data.question}
        ]
        
        if input_data.context:
            messages.append({
                "role": "user",
                "content": f"Additional context: {input_data.context}"
            })

        response = await openai.ChatCompletion.acreate(
            model=self.settings.openai_model,
            messages=messages,
            temperature=0.1,  # Low temperature for more deterministic SQL generation
            max_tokens=500
        )

        generated_sql = response.choices[0].message.content.strip()
        
        # Validate and modify query if needed
        if input_data.max_results:
            if "limit" not in generated_sql.lower():
                generated_sql += f"\nLIMIT {input_data.max_results}"

        # Execute query and get results
        try:
            results_df = self.database.execute_query(generated_sql)
            results = results_df.to_dict(orient="records")
            column_names = list(results_df.columns)
            row_count = len(results)
        except Exception as e:
            self.logger.error(f"Query execution failed: {str(e)}")
            raise RuntimeError(f"Failed to execute query: {str(e)}")

        execution_time = time.time() - start_time

        return SQLChatResponse(
            question=input_data.question,
            generated_sql=generated_sql,
            results=results,
            column_names=column_names,
            execution_time=execution_time,
            row_count=row_count
        ).dict()

    async def get_schema_overview(self) -> Dict[str, Any]:
        """Get an overview of the database schema.
        
        Returns:
            Dict containing schema information and sample data
        """
        return {
            "schema": self.schema.dict(),
            "sample_data": self.database.get_sample_data(3).to_dict(orient="records")
        }

    async def suggest_questions(self, n: int = 3) -> List[str]:
        """Generate suggested questions based on the schema.
        
        Args:
            n: Number of questions to generate
            
        Returns:
            List of suggested questions
        """
        schema_str = json.dumps(self.schema.dict(), indent=2)
        
        prompt = f"""Given this database schema:

{schema_str}

Generate {n} interesting analytical questions that could be answered using this data.
Return only the questions, one per line, without numbering or additional text."""

        response = await openai.ChatCompletion.acreate(
            model=self.settings.openai_model,
            messages=[
                {"role": "system", "content": "You are a data analyst helping to explore a dataset."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )

        questions = response.choices[0].message.content.strip().split("\n")
        return [q.strip() for q in questions if q.strip()]