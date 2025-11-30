# Job Scraper - LinkedIn & Computrabajo

A Python-based web scraper to search for job opportunities on LinkedIn and Computrabajo, with filtering by company ratings and salary information.

## Features

### Computrabajo Scraper

- 🔍 Search jobs by keyword
- ⭐ Filter by company rating/score
- 💰 Extract salary information when available
- 📊 Sort results by company rating (highest first)
- 🎯 Only returns positions with both company score and salary

### LinkedIn Scraper

- 🔍 Search jobs by position
- 🔐 Session management with cookie persistence
- 📍 Extract job title, company, location, and URL

## Installation

1. Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/linkedinSearcher.git
cd linkedinSearcher
```

2. Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Install Playwright browsers:

```bash
playwright install chromium
```

## Usage

### Computrabajo Scraper

```python
import asyncio
from computrabajo_searcher import ComputrabajoScraper

async def main():
    scraper = ComputrabajoScraper()
    results = await scraper.search("Desarrollador", limit=10)
    
    for job in results:
        print(f"{job['title']} at {job['company']}")
        print(f"Score: {job['score']} | Salary: {job['salary']}")
        print(f"URL: {job['url']}\n")

asyncio.run(main())
```

### LinkedIn Scraper

```python
import asyncio
from linkedin_scrapper import LinkedInScraper

async def main():
    scraper = LinkedInScraper()
    jobs = await scraper.search("Software Engineer", limit=10)
    
    for job in jobs:
        print(f"{job['title']} at {job['company']}")
        print(f"Location: {job['location']}")
        print(f"URL: {job['url']}\n")

asyncio.run(main())
```

**Note**: For LinkedIn, you'll need to log in manually the first time. The scraper will save your session cookies for future use.

## Project Structure

```
linkedinSearcher/
├── computrabajo_searcher.py  # Computrabajo scraper
├── linkedin_scrapper.py      # LinkedIn scraper
├── linkedin_searcher.py      # Legacy LinkedIn scraper
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## Requirements

- Python 3.8+
- playwright
- asyncio

## Output Format

### Computrabajo Results

```json
{
  "title": "Desarrollador Full Stack",
  "company": "Tech Company S.A.S",
  "location": "Bogotá, D.C.",
  "score": 4.6,
  "salary": "$ 3.500.000,00 (Mensual)",
  "url": "https://co.computrabajo.com/..."
}
```

### LinkedIn Results

```json
{
  "title": "Software Engineer",
  "company": "Tech Corp",
  "location": "Remote",
  "url": "https://www.linkedin.com/jobs/..."
}
```

## Notes

- **Computrabajo**: Only returns jobs with both company rating and salary information
- **LinkedIn**: Requires manual login on first use; cookies are saved for subsequent runs
- **Rate Limiting**: Be respectful of the websites' resources and don't scrape too aggressively

## License

MIT License

## Author

Santiago Perez (<santipego0001@gmail.com>)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
