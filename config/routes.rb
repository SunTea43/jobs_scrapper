Rails.application.routes.draw do
  resources :jobs do
    collection do
      post :scrape
    end
    member do
      patch :update_status
    end
  end

  root "jobs#index"
end
