require 'hocon'
require 'hocon/config_factory'

APP_CONFIG = Hocon::ConfigFactory.parse_file("#{Rails.root}/config/application.conf")

# Configure Azure OpenAI
OpenAI.configure do |config|
  config.access_token = APP_CONFIG['azure.openai.api_key']
  config.api_type = :azure
  config.api_version = APP_CONFIG['azure.openai.api_version']
  config.azure_api_base = APP_CONFIG['azure.openai.api_base']
end