import asyncio
from playwright.async_api import async_playwright
import json

class IndeedScraper:
    BASE_URL = "https://co.indeed.com/jobs?q={}&l={}"

    async def get_text(self, parent, selector):
        """Helper to get text or None"""
        el = await parent.query_selector(selector)
        if not el:
            return None
        return await el.evaluate("el => el.innerText.trim()")

    async def get_href(self, parent, selector):
        """Helper to get href or None"""
        el = await parent.query_selector(selector)
        if not el:
            return None
        return await el.evaluate("el => el.href")

    async def search(self, keyword: str, location: str = "Colombia", limit: int = 10):
        # Format keyword for Indeed URL (using + for spaces)
        query = keyword.replace(" ", "+")
        loc = location.replace(" ", "+")
        url = self.BASE_URL.format(query, loc)

        async with async_playwright() as p:
            # Launch in headless mode to match computrabajo_searcher.py
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(
                user_agent=(
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0 Safari/537.36"
                )
            )

            print(f"🔎 Loading Indeed results for: {keyword} in {location} …")
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            except Exception as e:
                print(f"⚠️ Error loading page: {e}")
                await browser.close()
                return []

            # Wait for job container to be present
            try:
                await page.wait_for_selector(".job_seen_beacon", timeout=15000)
            except:
                print("⚠️ No results found or page blocked.")
                await browser.close()
                return []

            # Scroll to trigger lazy loading if any
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
            await page.wait_for_timeout(1000)

            jobs = await page.query_selector_all(".job_seen_beacon")
            results = []

            for idx, job in enumerate(jobs):
                if idx >= limit:
                    break

                title = await self.get_text(job, "a.jcs-JobTitle")
                company = await self.get_text(job, '[data-testid="company-name"]')
                loc_text = await self.get_text(job, '[data-testid="text-location"]')
                link = await self.get_href(job, "a.jcs-JobTitle")
                
                # Extract salary if available
                salary = await self.get_text(job, '[data-testid="attribute_snippet-salary"]')
                if not salary:
                    salary = await self.get_text(job, ".salary-snippet-container")

                # Note: Indeed ratings are often dynamic, adding a basic capture if present
                rating_text = await self.get_text(job, ".ratingNumber")
                rating = float(rating_text.replace(",", ".")) if rating_text else 0.0

                results.append({
                    "title": title,
                    "company": company,
                    "location": loc_text,
                    "salary": salary,
                    "rating": rating,
                    "url": link
                })

            await browser.close()
            return results


import sys

async def main():
    keyword = sys.argv[1] if len(sys.argv) > 1 else "Diseñador Gráfico"
    location = sys.argv[2] if len(sys.argv) > 2 else "Colombia"
    
    scraper = IndeedScraper()
    results = await scraper.search(keyword, location=location, limit=10)
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
