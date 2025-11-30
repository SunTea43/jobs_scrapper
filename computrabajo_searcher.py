import asyncio
from playwright.async_api import async_playwright
import json

class ComputrabajoScraper:
    BASE_URL = "https://co.computrabajo.com/trabajo-de-{}"

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

    async def search(self, keyword: str, limit: int = 20):
        keyword_slug = keyword.lower().replace(" ", "-")
        url = self.BASE_URL.format(keyword_slug)

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(
                user_agent=(
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0 Safari/537.36"
                )
            )

            print(f"🔎 Loading Computrabajo results for: {keyword} …")
            await page.goto(url, wait_until="networkidle")
            
            # Scroll to bottom to trigger lazy loading
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(1000)  # Wait for content to load

            jobs = await page.query_selector_all("//article[contains(@class,'box_offer')]")
            results = []

            for idx, job in enumerate(jobs):
                if idx >= limit:
                    break

                title = await self.get_text(job, ".js-o-link")
                company = await self.get_text(job, ".item_company")
                # Fallback for company if .item_company fails (based on HTML analysis)
                if not company:
                    company = await self.get_text(job, "a[offer-grid-article-company-url]")
                
                location = await self.get_text(job, ".item_location")
                # Fallback for location
                if not location:
                    location = await self.get_text(job, "p.fs16.fc_base.mt5:not(.dFlex) > span.mr10")

                link = await self.get_href(job, ".js-o-link")
                score_text = await self.get_text(job, ".fx_none .fwB")
                score = float(score_text.replace(",", ".")) if score_text else 0.0

                # Extract salary - look for the salary icon and get parent text
                salary = None
                salary_icon = await job.query_selector(".i_salary")
                if salary_icon:
                    # Get the parent span's text
                    parent = await salary_icon.evaluate_handle("el => el.parentElement")
                    salary_text = await parent.evaluate("el => el.textContent")
                    if salary_text:
                        salary = salary_text.strip()

                # Filter: Only include companies with a score AND salary
                if score > 0 and salary:
                    results.append({
                        "title": title,
                        "company": company,
                        "location": location,
                        "score": score,
                        "salary": salary,
                        "url": link
                    })
            
            # Sort by score descending
            results.sort(key=lambda x: x["score"], reverse=True)

            await browser.close()
            return results


async def main():
    scraper = ComputrabajoScraper()
    results = await scraper.search("Desarrollador", limit=10)
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
