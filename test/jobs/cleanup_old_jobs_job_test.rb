require "test_helper"

class CleanupOldJobsJobTest < ActiveJob::TestCase
  test "removes jobs older than 1 week" do
    # Create an old job (8 days ago)
    old_job = Job.create!(
      title: "Old Job",
      company: "Company",
      url: "http://old.com",
      created_at: 8.days.ago
    )

    # Create a new job (today)
    new_job = Job.create!(
      title: "New Job",
      company: "Company",
      url: "http://new.com",
      created_at: Time.current
    )

    assert_difference "Job.count", -1 do
      CleanupOldJobsJob.perform_now
    end

    assert_not Job.exists?(old_job.id)
    assert Job.exists?(new_job.id)
  end
end
