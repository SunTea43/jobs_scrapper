class ScrapeJobsJob < ApplicationJob
  queue_as :default

  def perform(keyword)
    JobScraperService.call(keyword)
  end
end
