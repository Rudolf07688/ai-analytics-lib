import React from 'react';
import {
  Box,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Text,
  VStack,
  Badge,
} from '@chakra-ui/react';
import { SchemaResponse } from '../types';

interface Props {
  schema: SchemaResponse;
}

export const SchemaViewer: React.FC<Props> = ({ schema }) => {
  return (
    <VStack spacing={4} align="stretch">
      <Box>
        <Text fontSize="lg" fontWeight="bold">
          Table: {schema.schema.name}
        </Text>
        {schema.schema.description && (
          <Text fontSize="sm" color="gray.600">
            {schema.schema.description}
          </Text>
        )}
      </Box>

      <Box>
        <Text fontSize="sm" fontWeight="bold" mb={2}>
          Schema:
        </Text>
        <Table variant="simple" size="sm">
          <Thead>
            <Tr>
              <Th>Column</Th>
              <Th>Type</Th>
              <Th>Nullable</Th>
            </Tr>
          </Thead>
          <Tbody>
            {schema.schema.columns.map((col) => (
              <Tr key={col.name}>
                <Td>{col.name}</Td>
                <Td>
                  <Badge colorScheme="blue">{col.type}</Badge>
                </Td>
                <Td>
                  {col.nullable ? (
                    <Badge colorScheme="yellow">Nullable</Badge>
                  ) : (
                    <Badge colorScheme="green">Required</Badge>
                  )}
                </Td>
              </Tr>
            ))}
          </Tbody>
        </Table>
      </Box>

      <Box>
        <Text fontSize="sm" fontWeight="bold" mb={2}>
          Sample Data:
        </Text>
        <Box overflowX="auto">
          <Table variant="simple" size="sm">
            <Thead>
              <Tr>
                {schema.schema.columns.map((col) => (
                  <Th key={col.name}>{col.name}</Th>
                ))}
              </Tr>
            </Thead>
            <Tbody>
              {schema.sample_data.map((row, i) => (
                <Tr key={i}>
                  {schema.schema.columns.map((col) => (
                    <Td key={col.name}>{String(row[col.name])}</Td>
                  ))}
                </Tr>
              ))}
            </Tbody>
          </Table>
        </Box>
      </Box>
    </VStack>
  );
};