import axios from 'axios';
import { DatabaseConfig, QueryRequest, QueryResponse, SchemaResponse } from './types';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const executeQuery = async (
  config: DatabaseConfig,
  request: QueryRequest
): Promise<QueryResponse> => {
  const response = await api.post('/query', { ...config, ...request });
  return response.data;
};

export const getSchema = async (config: DatabaseConfig): Promise<SchemaResponse> => {
  const response = await api.get('/schema', { data: config });
  return response.data;
};

export const getSuggestedQuestions = async (
  config: DatabaseConfig,
  n: number = 3
): Promise<string[]> => {
  const response = await api.get('/suggest-questions', {
    params: { n },
    data: config,
  });
  return response.data;
};