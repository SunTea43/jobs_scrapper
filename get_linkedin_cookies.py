import asyncio
import json
from playwright.async_api import async_playwright

COOKIES_FILE = "linkedin_cookies.json"

async def get_cookies():
    print("\n🚀 Iniciando navegador para capturar cookies de LinkedIn...")
    print("👉 Por favor, inicia sesión manualmente en la ventana que se abrirá.")
    print("👉 Una vez veas tu feed de LinkedIn, regresa aquí.")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False) # Necesitamos ver la ventana
        context = await browser.new_context()
        page = await context.new_page()
        
        await page.goto("https://www.linkedin.com/login")
        
        # Esperamos a que el usuario navegue hasta el feed (identificamos el buscador global)
        try:
            # Timeout de 2 minutos para que el usuario tenga tiempo de loguearse y resolver captchas
            await page.wait_for_selector(".global-nav__search", timeout=120000)
            
            print("\n✅ ¡Sesión detectada exitosamente!")
            
            # Guardamos las cookies
            cookies = await context.cookies()
            with open(COOKIES_FILE, "w") as f:
                f.write(json.dumps(cookies, indent=2))
            
            print(f"💾 Cookies guardadas en: {COOKIES_FILE}")
            print("✨ Ahora LinkedIn funcionará automáticamente en segundo plano.")
            
        except Exception as e:
            print("\n❌ Error o tiempo de espera agotado. No se capturaron las cookies.")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(get_cookies())
