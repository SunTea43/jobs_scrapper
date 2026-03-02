class Job < ApplicationRecord
  validates :url, presence: true, format: { with: %r{\Ahttps?://.*\z}i, message: "must be a valid http or https URL" }

  enum :status, { pending: 0, applied: 1, rejected: 2, ignored: 3 }, default: :pending

  def safe_url
    url if url&.match?(%r{\Ahttps?://}i)
  end
end
