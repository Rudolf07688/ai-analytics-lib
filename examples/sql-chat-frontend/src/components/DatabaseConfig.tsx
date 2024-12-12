import React from 'react';
import {
  Box,
  FormControl,
  FormLabel,
  Input,
  Select,
  VStack,
  Button,
  useToast,
} from '@chakra-ui/react';
import { DatabaseConfig as DatabaseConfigType } from '../types';

interface Props {
  config: DatabaseConfigType;
  onConfigChange: (config: DatabaseConfigType) => void;
  onConnect: () => void;
}

export const DatabaseConfig: React.FC<Props> = ({
  config,
  onConfigChange,
  onConnect,
}) => {
  const toast = useToast();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    onConfigChange({ ...config, [name]: value });
  };

  const handleConnect = () => {
    // Basic validation
    if (config.db_type === 'postgres') {
      if (!config.host || !config.database || !config.user || !config.password) {
        toast({
          title: 'Missing Fields',
          description: 'Please fill in all required PostgreSQL fields',
          status: 'error',
          duration: 3000,
        });
        return;
      }
    } else if (config.db_type === 'bigquery') {
      if (!config.project_id || !config.dataset_id || !config.table_id) {
        toast({
          title: 'Missing Fields',
          description: 'Please fill in all required BigQuery fields',
          status: 'error',
          duration: 3000,
        });
        return;
      }
    }
    onConnect();
  };

  return (
    <Box p={4} borderWidth={1} borderRadius="lg">
      <VStack spacing={4} align="stretch">
        <FormControl>
          <FormLabel>Database Type</FormLabel>
          <Select name="db_type" value={config.db_type} onChange={handleChange}>
            <option value="postgres">PostgreSQL</option>
            <option value="bigquery">BigQuery</option>
          </Select>
        </FormControl>

        {config.db_type === 'postgres' ? (
          <>
            <FormControl>
              <FormLabel>Host</FormLabel>
              <Input name="host" value={config.host || ''} onChange={handleChange} />
            </FormControl>
            <FormControl>
              <FormLabel>Port</FormLabel>
              <Input
                name="port"
                type="number"
                value={config.port || 5432}
                onChange={handleChange}
              />
            </FormControl>
            <FormControl>
              <FormLabel>Database</FormLabel>
              <Input
                name="database"
                value={config.database || ''}
                onChange={handleChange}
              />
            </FormControl>
            <FormControl>
              <FormLabel>User</FormLabel>
              <Input name="user" value={config.user || ''} onChange={handleChange} />
            </FormControl>
            <FormControl>
              <FormLabel>Password</FormLabel>
              <Input
                name="password"
                type="password"
                value={config.password || ''}
                onChange={handleChange}
              />
            </FormControl>
            <FormControl>
              <FormLabel>Schema</FormLabel>
              <Input
                name="schema"
                value={config.schema || 'public'}
                onChange={handleChange}
              />
            </FormControl>
            <FormControl>
              <FormLabel>Table</FormLabel>
              <Input name="table" value={config.table || ''} onChange={handleChange} />
            </FormControl>
          </>
        ) : (
          <>
            <FormControl>
              <FormLabel>Project ID</FormLabel>
              <Input
                name="project_id"
                value={config.project_id || ''}
                onChange={handleChange}
              />
            </FormControl>
            <FormControl>
              <FormLabel>Dataset ID</FormLabel>
              <Input
                name="dataset_id"
                value={config.dataset_id || ''}
                onChange={handleChange}
              />
            </FormControl>
            <FormControl>
              <FormLabel>Table ID</FormLabel>
              <Input
                name="table_id"
                value={config.table_id || ''}
                onChange={handleChange}
              />
            </FormControl>
          </>
        )}

        <Button colorScheme="blue" onClick={handleConnect}>
          Connect
        </Button>
      </VStack>
    </Box>
  );
};