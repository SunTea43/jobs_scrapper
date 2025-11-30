import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

COOKIES_FILE = "linkedin_cookies.json"


class LinkedInScraper:
    BASE_URL = "https://www.linkedin.com/jobs/search/?keywords="

    def __init__(self):
        self.cookies_loaded = False

    async def load_cookies(self, context):
        if Path(COOKIES_FILE).exists():
            cookies = json.loads(open(COOKIES_FILE).read())
            await context.add_cookies(cookies)
            self.cookies_loaded = True

    async def save_cookies(self, context):
        cookies = await context.cookies()
        with open(COOKIES_FILE, "w") as f:
            f.write(json.dumps(cookies, indent=2))

    async def ensure_logged_in(self, page):
        if "checkpoint" in page.url or "login" in page.url:
            print("⚠️ You must login manually once...")

            await page.goto("https://www.linkedin.com/login", wait_until="domcontentloaded")

            # Wait for user login
            await page.wait_for_selector("#global-nav-search", timeout=0)

            print("✅ Logged in. Saving cookies...")
            await self.save_cookies(page.context)

    async def search(self, position, limit=10):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()

            # Load session cookies (if any)
            await self.load_cookies(context)

            page = await context.new_page()

            url = self.BASE_URL + position.replace(" ", "%20")
            print(f"🔍 Searching: {url}")

            await page.goto(url, wait_until="domcontentloaded", timeout=60000)

            # If login required, handle and retry
            await self.ensure_logged_in(page)
            await page.goto(url, wait_until="domcontentloaded")

            await page.wait_for_selector(".jobs-search-results-list", timeout=30000)

            jobs = []

            items = await page.query_selector_all("ul.jobs-search-results__list li")

            for li in items[:limit]:
                title = await li.query_selector_eval("h3", "el => el.innerText") if await li.query_selector("h3") else None
                company = await li.query_selector_eval(".base-search-card__subtitle", "el => el.innerText") if await li.query_selector(".base-search-card__subtitle") else None
                location = await li.query_selector_eval(".job-search-card__location", "el => el.innerText") if await li.query_selector(".job-search-card__location") else None
                link = await li.query_selector_eval("a", "el => el.href") if await li.query_selector("a") else None

                jobs.append({
                    "title": title,
                    "company": company.strip() if company else None,
                    "location": location,
                    "url": link,
                })

            await browser.close()
            return jobs


async def main():
    scraper = LinkedInScraper()
    jobs = await scraper.search("Software Engineer", limit=10)
    print(json.dumps(jobs, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
