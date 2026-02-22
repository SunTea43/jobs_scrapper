require "csv"

class JobsController < ApplicationController
  before_action :set_job, only: %i[ show edit update destroy update_status ]

  # GET /jobs or /jobs.json
  def index
    @jobs = Job.all

    if params[:query].present?
      @jobs = @jobs.where("title ILIKE :q OR company ILIKE :q", q: "%#{params[:query]}%")
    end

    if params[:source].present?
      @jobs = @jobs.where(source: params[:source])
    end

    if params[:min_score].present?
      @jobs = @jobs.where("score >= ?", params[:min_score].to_f)
    end

    if params[:status].present?
      @jobs = @jobs.where(status: params[:status])
    else
      # Default: don't show ignored jobs in main view unless requested
      @jobs = @jobs.where.not(status: :ignored) unless request.format.csv? || request.format.xlsx?
    end

    @jobs = @jobs.order(score: :desc, created_at: :desc)
    @sources = Job.distinct.pluck(:source)

    respond_to do |format|
      format.html
      format.json
      format.csv do
        send_data jobs_to_csv(@jobs), filename: "jobs-#{Time.current.strftime('%Y%m%d_%H%M%S')}.csv"
      end
      format.xlsx do
        response.headers["Content-Disposition"] = "attachment; filename=\"jobs-#{Time.current.strftime('%Y%m%d_%H%M%S')}.xlsx\""
      end
    end
  end

  # PATCH /jobs/1/update_status
  def update_status
    if @job.update(status: params[:status])
      redirect_back fallback_location: jobs_path, notice: "Job marked as #{@job.status}."
    end
  end

  # POST /jobs/scrape
  def scrape
    keyword = params[:keyword]
    if keyword.present?
      ScrapeJobsJob.perform_later(keyword)
      redirect_to jobs_path, notice: "Scraping started for '#{keyword}'. Please refresh in a few moments."
    else
      redirect_to jobs_path, alert: "Please provide a keyword to search."
    end
  end

  # GET /jobs/1 or /jobs/1.json
  def show
  end

  # GET /jobs/new
  def new
    @job = Job.new
  end

  # GET /jobs/1/edit
  def edit
  end

  # POST /jobs or /jobs.json
  def create
    @job = Job.new(job_params)

    respond_to do |format|
      if @job.save
        format.html { redirect_to @job, notice: "Job was successfully created." }
        format.json { render :show, status: :created, location: @job }
      else
        format.html { render :new, status: :unprocessable_entity }
        format.json { render json: @job.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /jobs/1 or /jobs/1.json
  def update
    respond_to do |format|
      if @job.update(job_params)
        format.html { redirect_to @job, notice: "Job was successfully updated.", status: :see_other }
        format.json { render :show, status: :ok, location: @job }
      else
        format.html { render :edit, status: :unprocessable_entity }
        format.json { render json: @job.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /jobs/1 or /jobs/1.json
  def destroy
    @job.destroy!

    respond_to do |format|
      format.html { redirect_to jobs_path, notice: "Job was successfully destroyed.", status: :see_other }
      format.json { head :no_content }
    end
  end

  private

  def jobs_to_csv(jobs)
    CSV.generate(headers: true) do |csv|
      csv << [ "Title", "Company", "Location", "Salary", "Score", "Source", "Status", "URL", "Date Found" ]
      jobs.each do |job|
        csv << [ job.title, job.company, job.location, job.salary, job.score, job.source, job.status, job.url, job.created_at.to_date ]
      end
    end
  end

  # Use callbacks to share common setup or constraints between actions.
  def set_job
    @job = Job.find(params.expect(:id))
  end

  # Only allow a list of trusted parameters through.
  def job_params
    params.expect(job: [ :title, :company, :location, :salary, :url, :score, :source ])
  end
end
