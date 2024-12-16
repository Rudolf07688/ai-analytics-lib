module Api
  module V1
    class QueriesController < ApplicationController
      def schema
        bigquery = BigqueryService.new
        render json: { schema: bigquery.get_schema }
      end

      def sample_data
        bigquery = BigqueryService.new
        render json: { data: bigquery.get_sample_data }
      end

      def execute
        question = params[:question]
        return render json: { error: 'Question is required' }, status: :bad_request if question.blank?

        bigquery = BigqueryService.new
        openai = AzureOpenaiService.new
        
        schema = bigquery.get_schema
        sql_query = openai.generate_sql(question, schema)
        
        return render json: { error: 'Failed to generate SQL query' }, status: :unprocessable_entity if sql_query.blank?

        begin
          results = bigquery.execute_query(sql_query)
          render json: {
            query: sql_query,
            results: results
          }
        rescue => e
          render json: { error: e.message }, status: :unprocessable_entity
        end
      end
    end
  end
end