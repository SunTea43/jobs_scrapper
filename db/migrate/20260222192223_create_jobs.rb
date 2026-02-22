class CreateJobs < ActiveRecord::Migration[8.1]
  def change
    create_table :jobs do |t|
      t.string :title
      t.string :company
      t.string :location
      t.string :salary
      t.string :url
      t.float :score
      t.string :source

      t.timestamps
    end
  end
end
