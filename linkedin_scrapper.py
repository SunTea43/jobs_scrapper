import asyncio
import json
import sys
from pathlib import Path
from playwright.async_api import async_playwright

# File where session cookies are stored
COOKIES_FILE = "linkedin_cookies.json"

class LinkedInScraper:
    # Authenticated search URL
    BASE_URL = "https://www.linkedin.com/jobs/search/?keywords={}"

    async def load_cookies(self, context):
        if Path(COOKIES_FILE).exists():
            with open(COOKIES_FILE, "r") as f:
                cookies = json.loads(f.read())
                await context.add_cookies(cookies)
            return True
        return False

    async def search(self, keyword, limit=10):
        async with async_playwright() as p:
            # Headless=True for background jobs (requires cookies)
            # If no cookies, it will fail, which is expected for automated tasks
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            )

            has_cookies = await self.load_cookies(context)
            if not has_cookies:
                print("❌ LinkedIn Cookies not found. Please run 'python get_linkedin_cookies.py' first.")
                await browser.close()
                return []

            page = await context.new_page()
            url = self.BASE_URL.format(keyword.replace(" ", "%20"))
            
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=60000)
                
                # Check if we were redirected to login (expired cookies)
                if "login" in page.url or "checkpoint" in page.url:
                    print("❌ LinkedIn session expired. Please run the login script again.")
                    await browser.close()
                    return []

                # Wait for results
                await page.wait_for_selector(".jobs-search-results-list", timeout=20000)
                
                # Small scroll to trigger lazy loading
                await page.evaluate("window.scrollTo(0, 500)")
                await asyncio.sleep(2)

                items = await page.query_selector_all(".jobs-search-results-list li.jobs-search-results-list__item")
                jobs = []

                for li in items[:limit]:
                    title_el = await li.query_selector(".job-card-list__title")
                    company_el = await li.query_selector(".job-card-container__primary-description")
                    location_el = await li.query_selector(".job-card-container__metadata-item")
                    link_el = await li.query_selector("a.job-card-list__title")

                    if title_el and link_el:
                        title = await title_el.inner_text()
                        company = await company_el.inner_text() if company_el else "Unknown"
                        location = await location_el.inner_text() if location_el else "Remote"
                        link = await link_el.get_attribute("href")
                        
                        # Normalize URL
                        if link and link.startswith("/"):
                            link = "https://www.linkedin.com" + link

                        jobs.append({
                            "title": title.strip(),
                            "company": company.strip(),
                            "location": location.strip(),
                            "url": link,
                            "salary": None,
                            "score": 0.0
                        })

                await browser.close()
                return jobs

            except Exception as e:
                print(f"⚠️ Error during LinkedIn search: {e}")
                await browser.close()
                return []

async def main():
    keyword = sys.argv[1] if len(sys.argv) > 1 else "Software Engineer"
    scraper = LinkedInScraper()
    results = await scraper.search(keyword, limit=10)
    print(json.dumps(results, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main())
