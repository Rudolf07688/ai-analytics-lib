Rails.application.routes.draw do
  # Health check endpoint
  get "up" => "rails/health#show", as: :rails_health_check

  # API endpoints
  namespace :api do
    namespace :v1 do
      get 'schema', to: 'queries#schema'
      get 'sample_data', to: 'queries#sample_data'
      post 'execute', to: 'queries#execute'
    end
  end
end
