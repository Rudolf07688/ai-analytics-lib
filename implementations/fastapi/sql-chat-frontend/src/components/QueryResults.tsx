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
} from '@chakra-ui/react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { QueryResponse } from '../types';

interface Props {
  response: QueryResponse;
}

export const QueryResults: React.FC<Props> = ({ response }) => {
  return (
    <VStack spacing={4} align="stretch">
      <Box>
        <Text fontSize="sm" fontWeight="bold" mb={2}>
          Generated SQL:
        </Text>
        <SyntaxHighlighter language="sql" style={vscDarkPlus}>
          {response.generated_sql}
        </SyntaxHighlighter>
      </Box>

      <Box>
        <Text fontSize="sm" fontWeight="bold" mb={2}>
          Results ({response.row_count} rows, {response.execution_time.toFixed(2)}s):
        </Text>
        <Box overflowX="auto">
          <Table variant="simple" size="sm">
            <Thead>
              <Tr>
                {response.column_names.map((col) => (
                  <Th key={col}>{col}</Th>
                ))}
              </Tr>
            </Thead>
            <Tbody>
              {response.results.map((row, i) => (
                <Tr key={i}>
                  {response.column_names.map((col) => (
                    <Td key={col}>{String(row[col])}</Td>
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