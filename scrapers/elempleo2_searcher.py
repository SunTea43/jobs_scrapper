import urllib.request
import urllib.parse
import json
import re
import sys

class ElEmpleoAlternativeScraper:
    BASE_URL = "https://www.elempleo.com/co/ofertas-empleo?trabajo={}"

    def search(self, keyword, limit=15):
        query = urllib.parse.quote(keyword.replace(" ", "-"))
        url = self.BASE_URL.format(query)

        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"}
        )
        
        try:
            print(f"🔎 Loading El Empleo (Alternative) results for: {keyword} …", file=sys.stderr)
            with urllib.request.urlopen(req, timeout=30) as response:
                html = response.read().decode('utf-8')
        except Exception as e:
            print(f"⚠️ Error: {e}", file=sys.stderr)
            return []

        results = []
        
        # Extract data-ga4-offerdata and data-url
        # <div class="js-area-bind area-bind" data-url="/co/ofertas-trabajo/desarrollador-net-1886040988?trabajo=desarrollador" data-ga4-offerdata="{...}"
        
        pattern = re.compile(r'data-url="([^"]+)"\s+data-ga4-offerdata="([^"]+)"')
        matches = pattern.findall(html)
        
        import html as html_parser
        
        for idx, (data_url, ga4_data_str) in enumerate(matches):
            if idx >= limit:
                break
                
            try:
                ga4_data_str = html_parser.unescape(ga4_data_str)
                ga4_data = json.loads(ga4_data_str)
                
                # Correct the relative URL
                full_url = data_url
                if full_url.startswith("/"):
                    full_url = "https://www.elempleo.com" + full_url
                
                results.append({
                    "title": ga4_data.get("title", ""),
                    "company": ga4_data.get("company", ""),
                    "location": ga4_data.get("location", ""),
                    "salary": ga4_data.get("salary", ""),
                    "url": full_url,
                    "score": 0.0
                })
            except Exception as e:
                continue

        return results

def main():
    keyword = sys.argv[1] if len(sys.argv) > 1 else "Desarrollador"
    scraper = ElEmpleoAlternativeScraper()
    results = scraper.search(keyword, limit=10)
    print(json.dumps(results, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
