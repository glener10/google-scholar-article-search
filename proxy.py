from scholarly import ProxyGenerator
import os

def config_proxy():
  pg = ProxyGenerator()
  scraper_api_key = os.getenv('SCRAPER_API_KEY')
  if not scraper_api_key:
    raise Exception("❌ missing SCRAPER_API_KEY in .env")
  pg.ScraperAPI(scraper_api_key)
  return pg