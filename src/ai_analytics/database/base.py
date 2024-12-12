"""Base database connection interface."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

import pandas as pd
from pydantic import BaseModel


class TableSchema(BaseModel):
    """Schema information for a database table."""
    
    name: str
    columns: List[Dict[str, str]]
    description: Optional[str] = None


class DatabaseConnection(ABC):
    """Abstract base class for database connections."""

    @abstractmethod
    def connect(self) -> None:
        """Establish connection to the database."""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Close the database connection."""
        pass

    @abstractmethod
    def execute_query(self, query: str) -> pd.DataFrame:
        """Execute a SQL query and return results as a DataFrame.
        
        Args:
            query: SQL query string to execute.
            
        Returns:
            DataFrame containing query results.
        """
        pass

    @abstractmethod
    def get_schema(self) -> TableSchema:
        """Get schema information for the configured table.
        
        Returns:
            TableSchema containing table information.
        """
        pass

    @abstractmethod
    def get_sample_data(self, limit: int = 5) -> pd.DataFrame:
        """Get sample data from the table.
        
        Args:
            limit: Maximum number of rows to return.
            
        Returns:
            DataFrame containing sample data.
        """
        pass

    def validate_query(self, query: str) -> bool:
        """Basic validation of SQL query.
        
        Args:
            query: SQL query string to validate.
            
        Returns:
            True if query appears valid, False otherwise.
        """
        # Basic validation - can be extended in subclasses
        query = query.lower().strip()
        if not query:
            return False
        
        # Check for basic SQL structure
        valid_starts = ['select', 'with', '(']
        if not any(query.startswith(start) for start in valid_starts):
            return False
            
        return True