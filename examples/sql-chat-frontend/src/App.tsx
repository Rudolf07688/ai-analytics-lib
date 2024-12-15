import React, { useState } from 'react';
import {
  ChakraProvider,
  Container,
  VStack,
  Heading,
  useToast,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
} from '@chakra-ui/react';
import { DatabaseConfig } from './components/DatabaseConfig';
import { QueryInput } from './components/QueryInput';
import { QueryResults } from './components/QueryResults';
import { SchemaViewer } from './components/SchemaViewer';
import { DatabaseConfig as DatabaseConfigType, QueryRequest, QueryResponse, SchemaResponse } from './types';
import { executeQuery, getSchema, getSuggestedQuestions } from './api';

function App() {
  const toast = useToast();
  const [dbConfig, setDbConfig] = useState<DatabaseConfigType>({
    db_type: 'postgres',
  });
  const [isConnected, setIsConnected] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [schema, setSchema] = useState<SchemaResponse | null>(null);
  const [suggestedQuestions, setSuggestedQuestions] = useState<string[]>([]);
  const [queryResponse, setQueryResponse] = useState<QueryResponse | null>(null);

  const handleConnect = async () => {
    setIsLoading(true);
    try {
      const schemaData = await getSchema(dbConfig);
      setSchema(schemaData);
      
      const questions = await getSuggestedQuestions(dbConfig);
      setSuggestedQuestions(questions);
      
      setIsConnected(true);
      toast({
        title: 'Connected',
        description: 'Successfully connected to database',
        status: 'success',
        duration: 3000,
      });
    } catch (error) {
      toast({
        title: 'Connection Failed',
        description: error instanceof Error ? error.message : 'Failed to connect to database',
        status: 'error',
        duration: 5000,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuery = async (request: QueryRequest) => {
    setIsLoading(true);
    try {
      const response = await executeQuery(dbConfig, request);
      setQueryResponse(response);
    } catch (error) {
      toast({
        title: 'Query Failed',
        description: error instanceof Error ? error.message : 'Failed to execute query',
        status: 'error',
        duration: 5000,
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <ChakraProvider>
      <Container maxW="container.xl" py={8}>
        <VStack spacing={8} align="stretch">
          <Heading>SQL Chat</Heading>

          {!isConnected ? (
            <DatabaseConfig
              config={dbConfig}
              onConfigChange={setDbConfig}
              onConnect={handleConnect}
            />
          ) : (
            <Tabs>
              <TabList>
                <Tab>Query</Tab>
                <Tab>Schema</Tab>
              </TabList>

              <TabPanels>
                <TabPanel>
                  <VStack spacing={6} align="stretch">
                    <QueryInput
                      onSubmit={handleQuery}
                      suggestedQuestions={suggestedQuestions}
                      isLoading={isLoading}
                    />
                    {queryResponse && <QueryResults response={queryResponse} />}
                  </VStack>
                </TabPanel>

                <TabPanel>
                  {schema && <SchemaViewer schema={schema} />}
                </TabPanel>
              </TabPanels>
            </Tabs>
          )}
        </VStack>
      </Container>
    </ChakraProvider>
  );
}

export default App;