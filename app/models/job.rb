class Job < ApplicationRecord
  enum :status, { pending: 0, applied: 1, rejected: 2, ignored: 3 }, default: :pending
end
