import asyncio
from playwright.async_api import async_playwright
import json
import sys

class LinkedInGuestScraper:
    # Public job search URL
    BASE_URL = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={}"

    async def get_text(self, parent, selector):
        el = await parent.query_selector(selector)
        return await el.evaluate("el => el.innerText.trim()") if el else None

    async def get_href(self, parent, selector):
        el = await parent.query_selector(selector)
        return await el.evaluate("el => el.href") if el else None

    async def search(self, keyword, limit=10):
        url = self.BASE_URL.format(keyword.replace(" ", "%20"))

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )

            print(f"🔎 Loading LinkedIn Guest results for: {keyword} …")
            try:
                # LinkedIn guest search often works with simple requests but we use playwright to be safer
                await page.goto(url, wait_until="domcontentloaded", timeout=60000)
                # The guest API returns HTML fragments (li tags)
                items = await page.query_selector_all("li")
            except Exception as e:
                print(f"⚠️ Error: {e}")
                await browser.close()
                return []

            results = []
            for idx, item in enumerate(items):
                if idx >= limit:
                    break

                title = await self.get_text(item, ".base-search-card__title")
                company = await self.get_text(item, ".base-search-card__subtitle")
                location = await self.get_text(item, ".job-search-card__location")
                link = await self.get_href(item, "a.base-card__full-link")

                if title and link:
                    results.append({
                        "title": title,
                        "company": company,
                        "location": location,
                        "url": link,
                        "salary": None,
                        "score": 0.0
                    })

            await browser.close()
            return results

async def main():
    keyword = sys.argv[1] if len(sys.argv) > 1 else "Software Engineer"
    scraper = LinkedInGuestScraper()
    results = await scraper.search(keyword, limit=10)
    print(json.dumps(results, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main())
