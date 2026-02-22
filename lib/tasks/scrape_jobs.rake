namespace :jobs do
  desc "Fetch jobs from scrapers"
  task :fetch, [ :keyword ] => :environment do |t, args|
    keyword = args[:keyword] || "Software Engineer"
    puts "Fetching jobs for '#{keyword}'..."
    JobScraperService.call(keyword)
    puts "Done."
  end
end
