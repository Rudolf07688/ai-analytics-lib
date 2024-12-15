import React, { useState } from 'react';
import {
  Box,
  Button,
  Textarea,
  VStack,
  HStack,
  Text,
  useToast,
} from '@chakra-ui/react';
import { QueryRequest } from '../types';

interface Props {
  onSubmit: (request: QueryRequest) => void;
  suggestedQuestions: string[];
  isLoading: boolean;
}

export const QueryInput: React.FC<Props> = ({
  onSubmit,
  suggestedQuestions,
  isLoading,
}) => {
  const [question, setQuestion] = useState('');
  const toast = useToast();

  const handleSubmit = () => {
    if (!question.trim()) {
      toast({
        title: 'Empty Question',
        description: 'Please enter a question',
        status: 'error',
        duration: 3000,
      });
      return;
    }

    onSubmit({
      question: question.trim(),
      max_results: 100,
    });
  };

  const handleSuggestedQuestion = (q: string) => {
    setQuestion(q);
    onSubmit({
      question: q,
      max_results: 100,
    });
  };

  return (
    <Box>
      <VStack spacing={4} align="stretch">
        <Textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question about your data..."
          size="lg"
          rows={3}
        />
        
        <Button
          colorScheme="blue"
          onClick={handleSubmit}
          isLoading={isLoading}
          loadingText="Analyzing..."
        >
          Ask Question
        </Button>

        {suggestedQuestions.length > 0 && (
          <Box>
            <Text fontSize="sm" fontWeight="bold" mb={2}>
              Suggested Questions:
            </Text>
            <VStack align="stretch" spacing={2}>
              {suggestedQuestions.map((q, index) => (
                <Button
                  key={index}
                  variant="outline"
                  size="sm"
                  onClick={() => handleSuggestedQuestion(q)}
                  isDisabled={isLoading}
                >
                  {q}
                </Button>
              ))}
            </VStack>
          </Box>
        )}
      </VStack>
    </Box>
  );
};