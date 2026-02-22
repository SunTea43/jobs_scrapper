class CleanupOldJobsJob < ApplicationJob
  queue_as :default

  def perform
    # Delete jobs created more than 1 week ago
    count = Job.where("created_at < ?", 1.week.ago).delete_all
    Rails.logger.info "CleanupOldJobsJob: Deleted #{count} old job(s)."
  end
end
