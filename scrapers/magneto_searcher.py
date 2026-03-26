import asyncio
from playwright.async_api import async_playwright
import json
import sys

class MagnetoScraper:
    BASE_URL = "https://www.magneto365.com/co/trabajos/buscar/{}"

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
        # Format keyword for Magneto URL (using - for spaces)
        query = keyword.lower().strip().replace(" ", "-")
        url = self.BASE_URL.format(query)

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
            )
            page = await context.new_page()

            print(f"🔎 Loading Magneto results for: {keyword} …")
            try:
                # Go to page and wait for results to load
                await page.goto(url, wait_until="networkidle", timeout=60000)
                
                # Check for either 'article' or the 'no results' text
                try:
                    # In Playwright, can wait for results or specific text
                    await page.wait_for_selector("article, text=/No encontramos resultados/", timeout=15000)
                except Exception:
                    # If both fail, we might still have something, so proceed to checks below
                    pass

                # Check for "No encontramos resultados" text specifically
                no_results = await page.query_selector("text=/No encontramos resultados/")
                if no_results:
                    print(f"ℹ️ No results found on Magneto for '{keyword}'")
                    await browser.close()
                    return []

                # Final check for job elements
                job_elements = await page.query_selector_all("article")
                if not job_elements:
                    # Try waiting one more time for selector article if nothing was found yet
                    try:
                        await page.wait_for_selector("article", timeout=5000)
                        job_elements = await page.query_selector_all("article")
                    except:
                        pass
                
                if not job_elements:
                    print(f"⚠️ No job results or results message found for '{keyword}'")
                    await browser.close()
                    return []
            except Exception as e:
                print(f"⚠️ Error during search: {e}")
                await browser.close()
                return []

            # Scroll to trigger lazy loading
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
            await page.wait_for_timeout(2000)

            job_elements = await page.query_selector_all("article")
            results = []

            for idx, job in enumerate(job_elements):
                if idx >= limit:
                    break

                # Extract title and link
                title = await self.get_text(job, "h2 a")
                link = await self.get_href(job, "h2 a")

                # Extract company and contract type
                company_contract = await self.get_text(job, "h3")
                company = company_contract.split("|")[0].strip() if company_contract else None
                contract = company_contract.split("|")[1].strip() if company_contract and "|" in company_contract else None

                # Extract salary and location
                # Based on analysis: p:nth-of-type(1) is salary, p:nth-of-type(2) is location
                salary_raw = await self.get_text(job, "p:nth-of-type(1)")
                location_raw = await self.get_text(job, "p:nth-of-type(2)")
                
                # Clean up trailing characters like commas that Magneto often leaves
                salary = salary_raw.rstrip(",").strip() if salary_raw else None
                location = location_raw.rstrip(",").strip() if location_raw else None
                
                # Check if we got something that looks like a job
                if title and link:
                    results.append({
                        "title": title,
                        "company": company,
                        "location": location,
                        "salary": salary,
                        "contract": contract,
                        "url": link,
                        "source": "Magneto"
                    })

            await browser.close()
            return results

async def main():
    keyword = sys.argv[1] if len(sys.argv) > 1 else "Software"
    scraper = MagnetoScraper()
    results = await scraper.search(keyword, limit=20)
    print(json.dumps(results, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main())
