"""BigQuery database connection implementation."""

import json
from typing import Any, Dict, Optional

import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

from ai_analytics.database.base import DatabaseConnection, TableSchema


class BigQueryConnection(DatabaseConnection):
    """Connection to Google BigQuery."""

    def __init__(
        self,
        project_id: str,
        dataset_id: str,
        table_id: str,
        credentials_json: Optional[str] = None,
    ):
        """Initialize BigQuery connection.
        
        Args:
            project_id: Google Cloud project ID.
            dataset_id: BigQuery dataset ID.
            table_id: BigQuery table ID.
            credentials_json: Optional service account credentials JSON string.
        """
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.credentials_json = credentials_json
        self.client = None
        self.table = None

    def connect(self) -> None:
        """Establish connection to BigQuery."""
        if self.credentials_json:
            credentials_info = json.loads(self.credentials_json)
            credentials = service_account.Credentials.from_service_account_info(
                credentials_info
            )
            self.client = bigquery.Client(
                credentials=credentials,
                project=self.project_id
            )
        else:
            self.client = bigquery.Client(project=self.project_id)
        
        dataset_ref = self.client.dataset(self.dataset_id)
        table_ref = dataset_ref.table(self.table_id)
        self.table = self.client.get_table(table_ref)

    def disconnect(self) -> None:
        """Close BigQuery connection."""
        if self.client:
            self.client.close()

    def execute_query(self, query: str) -> pd.DataFrame:
        """Execute BigQuery query.
        
        Args:
            query: SQL query string.
            
        Returns:
            DataFrame with query results.
        """
        if not self.client:
            self.connect()
            
        query_job = self.client.query(query)
        return query_job.to_dataframe()

    def get_schema(self) -> TableSchema:
        """Get BigQuery table schema.
        
        Returns:
            TableSchema containing column information.
        """
        if not self.table:
            self.connect()
            
        columns = [
            {"name": field.name, "type": field.field_type}
            for field in self.table.schema
        ]
        
        return TableSchema(
            name=f"{self.project_id}.{self.dataset_id}.{self.table_id}",
            columns=columns,
            description=self.table.description
        )

    def get_sample_data(self, limit: int = 5) -> pd.DataFrame:
        """Get sample data from BigQuery table.
        
        Args:
            limit: Maximum number of rows to return.
            
        Returns:
            DataFrame containing sample data.
        """
        query = f"""
        SELECT *
        FROM `{self.project_id}.{self.dataset_id}.{self.table_id}`
        LIMIT {limit}
        """
        return self.execute_query(query)