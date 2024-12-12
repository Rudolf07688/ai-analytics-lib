export interface DatabaseConfig {
  db_type: 'postgres' | 'bigquery';
  host?: string;
  port?: number;
  database?: string;
  user?: string;
  password?: string;
  schema?: string;
  table?: string;
  project_id?: string;
  dataset_id?: string;
  table_id?: string;
  credentials_json?: string;
}

export interface QueryRequest {
  question: string;
  context?: string;
  max_results?: number;
}

export interface QueryResponse {
  question: string;
  generated_sql: string;
  results: Record<string, any>[];
  column_names: string[];
  execution_time: number;
  row_count: number;
}

export interface SchemaColumn {
  name: string;
  type: string;
  nullable?: boolean;
}

export interface TableSchema {
  name: string;
  columns: SchemaColumn[];
  description?: string;
}

export interface SchemaResponse {
  schema: TableSchema;
  sample_data: Record<string, any>[];
}