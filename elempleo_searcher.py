import asyncio
from playwright.async_api import async_playwright
import json
import sys

class ElEmpleoScraper:
    BASE_URL = "https://www.elempleo.com/co/ofertas-empleo?trabajo={}"

    async def get_text(self, parent, selector):
        el = await parent.query_selector(selector)
        return await el.evaluate("el => el.innerText.trim()") if el else None

    async def get_href(self, parent, selector):
        el = await parent.query_selector(selector)
        return await el.evaluate("el => el.href") if el else None

    async def search(self, keyword, limit=15):
        query = keyword.replace(" ", "-")
        url = self.BASE_URL.format(query)

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
            )

            print(f"🔎 Loading El Empleo results for: {keyword} …")
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=60000)
                await page.wait_for_selector(".result-item", timeout=15000)
            except Exception as e:
                print(f"⚠️ Error: {e}")
                await browser.close()
                return []

            items = await page.query_selector_all(".result-item")
            results = []

            for idx, item in enumerate(items):
                if idx >= limit:
                    break

                title = await self.get_text(item, ".js-job-link")
                company = await self.get_text(item, ".info-company-name")
                location = await self.get_text(item, ".info-city")
                salary = await self.get_text(item, ".info-salary")
                link = await self.get_href(item, ".js-job-link")

                if title and link:
                    results.append({
                        "title": title,
                        "company": company,
                        "location": location,
                        "salary": salary,
                        "url": link,
                        "score": 0.0 # El Empleo doesn't easily show company rating in results
                    })

            await browser.close()
            return results

async def main():
    keyword = sys.argv[1] if len(sys.argv) > 1 else "Desarrollador"
    scraper = ElEmpleoScraper()
    results = await scraper.search(keyword, limit=10)
    print(json.dumps(results, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main())
