json.extract! job, :id, :title, :company, :location, :salary, :url, :score, :source, :created_at, :updated_at
json.url job_url(job, format: :json)
