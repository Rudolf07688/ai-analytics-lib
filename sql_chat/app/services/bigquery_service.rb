require 'google/cloud/bigquery'

class BigqueryService
  def initialize
    @client = Google::Cloud::Bigquery.new(
      project_id: APP_CONFIG['bigquery.project_id'],
      credentials: JSON.parse(APP_CONFIG['bigquery.credentials_json'])
    )
    @dataset = APP_CONFIG['bigquery.dataset']
    @table = APP_CONFIG['bigquery.table']
  end

  def execute_query(query)
    results = @client.query(query)
    results.map { |row| row.to_h }
  end

  def get_schema
    table = @client.dataset(@dataset).table(@table)
    table.schema.fields.map { |field| { name: field.name, type: field.type } }
  end

  def get_sample_data(limit = 5)
    query = "SELECT * FROM `#{APP_CONFIG['bigquery.project_id']}.#{@dataset}.#{@table}` LIMIT #{limit}"
    execute_query(query)
  end
end