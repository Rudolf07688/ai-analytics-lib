class AzureOpenaiService
  def initialize
    @deployment = APP_CONFIG['azure.openai.deployment_name']
  end

  def generate_sql(question, schema)
    system_prompt = <<~PROMPT
      You are a helpful SQL assistant that generates BigQuery SQL queries.
      Given the following schema, generate a SQL query that answers the user's question.
      
      Table Schema:
      #{schema.map { |field| "- #{field[:name]} (#{field[:type]})" }.join("\n")}
      
      Only return the SQL query without any explanation.
    PROMPT

    response = OpenAI::Client.new.chat(
      parameters: {
        model: @deployment,
        messages: [
          { role: "system", content: system_prompt },
          { role: "user", content: question }
        ],
        temperature: 0
      }
    )

    response.dig("choices", 0, "message", "content")
  end
end