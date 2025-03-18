from scholarly import ProxyGenerator
import os

def config_proxy(PROXY_TYPE):
  pg = ProxyGenerator()
  if PROXY_TYPE == "SCHOLARLY_FREE_PROXY":
    pg.FreeProxies()
    print(f"🛜 lib proxy configured 'pg.FreeProxies()'")
  elif PROXY_TYPE == "SCRAPER_API":
    scraper_api_key = os.getenv('SCRAPER_API_KEY')
    if not scraper_api_key:
      raise Exception("❌ missing SCRAPER_API_KEY in .env")
    pg.ScraperAPI(scraper_api_key)
  elif PROXY_TYPE == "MANUAL":
    manual_proxy = os.getenv("MANUAL_PROXY")
    if not manual_proxy:
      raise Exception("❌ missing MANUAL_PROXY in .env")
    pg.SingleProxy(manual_proxy)
  else:
    print("⚠️ invalid PROXY_TYPE, exiting...")
    exit(1)
  return pg