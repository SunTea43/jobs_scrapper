class JobScraperService
  def self.call(keyword)
    new(keyword).call
  end

  def initialize(keyword)
    @keyword = keyword
    @scrapers = [
      { name: "Indeed", script: "indeed_searcher.py" },
      { name: "Computrabajo", script: "computrabajo_searcher.py" },
      { name: "El Empleo", script: "elempleo_searcher.py" },
      { name: "LinkedIn", script: "linkedin_scrapper.py" }
    ]
  end

  def call
    @scrapers.each do |scraper|
      run_scraper(scraper)
    end
  end

  private

  def run_scraper(scraper)
    require "open3"
    python_bin = "./venv/bin/python"
    script_path = scraper[:script]

    begin
      output, status = Open3.capture3(python_bin, script_path, @keyword)

      if status.success?
        json_match = output.match(/\[.*\]/m)
        if json_match
          jobs_json = JSON.parse(json_match[0])
          jobs_json.each do |job_data|
            next unless job_data["title"] && job_data["url"]

            job = Job.find_or_initialize_by(url: job_data["url"])
            job.title = job_data["title"]
            job.company = job_data["company"]
            job.location = job_data["location"]
            job.salary = job_data["salary"]
            job.score = job_data["score"] || job_data["rating"] || 0.0
            job.source = scraper[:name]
            job.save!
          end
        end
      else
        Rails.logger.error "Scraper #{scraper[:name]} failed: #{output}"
      end
    rescue => e
      Rails.logger.error "Error running #{scraper[:name]}: #{e.message}"
    end
  end
end
