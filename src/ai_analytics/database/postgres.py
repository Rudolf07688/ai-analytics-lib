"""PostgreSQL database connection implementation."""

from typing import Any, Dict, Optional
from urllib.parse import quote_plus

import pandas as pd
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

from ai_analytics.database.base import DatabaseConnection, TableSchema


class PostgresConnection(DatabaseConnection):
    """Connection to PostgreSQL database."""

    def __init__(
        self,
        host: str,
        database: str,
        user: str,
        password: str,
        port: int = 5432,
        schema: str = "public",
        table: str = None,
        ssl_mode: Optional[str] = None,
    ):
        """Initialize PostgreSQL connection.
        
        Args:
            host: Database host address
            database: Database name
            user: Database user
            password: Database password
            port: Database port (default: 5432)
            schema: Database schema (default: public)
            table: Table name to query
            ssl_mode: SSL mode for connection (optional)
        """
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.schema = schema
        self.table = table
        self.ssl_mode = ssl_mode
        self.engine: Optional[Engine] = None

    def _build_connection_string(self) -> str:
        """Build PostgreSQL connection string.
        
        Returns:
            Connection string for SQLAlchemy
        """
        # URL encode the password to handle special characters
        encoded_password = quote_plus(self.password)
        
        conn_str = (
            f"postgresql://{self.user}:{encoded_password}@{self.host}:{self.port}/{self.database}"
        )
        
        if self.ssl_mode:
            conn_str += f"?sslmode={self.ssl_mode}"
            
        return conn_str

    def connect(self) -> None:
        """Establish connection to PostgreSQL."""
        try:
            conn_str = self._build_connection_string()
            self.engine = create_engine(conn_str)
            # Test connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
        except SQLAlchemyError as e:
            raise ConnectionError(f"Failed to connect to PostgreSQL: {str(e)}")

    def disconnect(self) -> None:
        """Close PostgreSQL connection."""
        if self.engine:
            self.engine.dispose()
            self.engine = None

    def execute_query(self, query: str) -> pd.DataFrame:
        """Execute PostgreSQL query.
        
        Args:
            query: SQL query string
            
        Returns:
            DataFrame with query results
        """
        if not self.engine:
            self.connect()
            
        try:
            return pd.read_sql_query(query, self.engine)
        except SQLAlchemyError as e:
            raise RuntimeError(f"Query execution failed: {str(e)}")

    def get_schema(self) -> TableSchema:
        """Get PostgreSQL table schema.
        
        Returns:
            TableSchema containing column information
            
        Raises:
            ValueError: If no table name is specified
        """
        if not self.table:
            raise ValueError("Table name must be specified")
            
        if not self.engine:
            self.connect()
            
        inspector = inspect(self.engine)
        columns = []
        
        for column in inspector.get_columns(self.table, schema=self.schema):
            columns.append({
                "name": column["name"],
                "type": str(column["type"]),
                "nullable": column["nullable"],
            })
            
        # Get table comment if available
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(f"""
                    SELECT obj_description('{self.schema}.{self.table}'::regclass, 'pg_class') as description
                """))
                description = result.scalar()
        except SQLAlchemyError:
            description = None
            
        return TableSchema(
            name=f"{self.schema}.{self.table}",
            columns=columns,
            description=description
        )

    def get_sample_data(self, limit: int = 5) -> pd.DataFrame:
        """Get sample data from PostgreSQL table.
        
        Args:
            limit: Maximum number of rows to return
            
        Returns:
            DataFrame containing sample data
            
        Raises:
            ValueError: If no table name is specified
        """
        if not self.table:
            raise ValueError("Table name must be specified")
            
        query = f"""
        SELECT *
        FROM {self.schema}.{self.table}
        LIMIT {limit}
        """
        return self.execute_query(query)

    def list_tables(self) -> list[str]:
        """Get list of tables in the specified schema.
        
        Returns:
            List of table names
        """
        if not self.engine:
            self.connect()
            
        inspector = inspect(self.engine)
        return inspector.get_table_names(schema=self.schema)

    def get_table_preview(self, table_name: str, schema: str = None) -> Dict[str, Any]:
        """Get a preview of table structure and sample data.
        
        Args:
            table_name: Name of the table to preview
            schema: Schema name (defaults to connection schema)
            
        Returns:
            Dict containing table information and sample data
        """
        original_table = self.table
        original_schema = self.schema
        
        try:
            self.table = table_name
            if schema:
                self.schema = schema
                
            return {
                "schema": self.get_schema().dict(),
                "sample_data": self.get_sample_data(3).to_dict(orient="records")
            }
        finally:
            self.table = original_table
            self.schema = original_schema