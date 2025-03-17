import pandas as pd
import time
from scholarly import ProxyGenerator, scholarly
import random
import os
from dotenv import load_dotenv
import datetime
import requests

start_time = datetime.datetime.now()
load_dotenv()

WAIT_TIME_PER_ARTICLE_SEARCH_SECONDS = 2
WAIT_TIME_PER_CSV_SAVE_SECONDS = 5

PROXY_TYPE = "LIB_FREE_PROXY" # NO_PROXY, GET_FREE_PROXY, LIB_FREE_PROXY, SCRAPER_API, MANUAL
CHANGE_PROXY_EVERY_N_ARTICLES = -1 # only works if PROXY_TYPE = "GET_FREE_PROXY"

SAVE_CSV_EVERY_N_ARTICLES = 50
OUTPUT_FILE = 'articles.csv'

STOP_IN_N_RESULTS = -1 # (only considered if is > 0)
INITIAL_SEARCH_YEAR = 2020
FINAL_SEARCH_YEAR = 2025
SEARCH_QUERY = '("security mechanisms" OR "protection mechanisms" OR "security measures" OR "security protocols" OR "fraud prevention") AND ("Brazilian instant payment" OR " instant payment system in Brazil" OR " PIX ") AND ("Brazil")'

print(f"🚀 Starting process at {start_time}")
print("🕒 Wait time configurations:")
print(f"  - Wait time per article search (seconds): {WAIT_TIME_PER_ARTICLE_SEARCH_SECONDS}")
print(f"  - Wait time per CSV save (seconds): {WAIT_TIME_PER_CSV_SAVE_SECONDS}")
print(f"🔧 Proxy configurations:")
print(f"  - Proxy type: {PROXY_TYPE} - Types availables: NO_PROXY, GET_FREE_PROXY, LIB_FREE_PROXY (default), SCRAPER_API, MANUAL")
print(f"  - Change proxy every N articles (only considered if (PROXY_TYPE = 'GET_FREE_PROXY' || 'LIB_FREE_PROXY') and CHANGE_PROXY_EVERY_N_ARTICLES > 0): {CHANGE_PROXY_EVERY_N_ARTICLES}")
print(f"💾 CSV configurations:")
print(f"  - Save CSV every N articles: {SAVE_CSV_EVERY_N_ARTICLES}")
print(f"  - Output file: {OUTPUT_FILE}")
print(f"🔎 Search configurations:")
print(f"  - Stop in N results (only considered if is > 0): {STOP_IN_N_RESULTS}")
print(f"  - Year Range: {INITIAL_SEARCH_YEAR} to {FINAL_SEARCH_YEAR}")
print(f"  - Search Query: {SEARCH_QUERY}\n")

def save_articles_csv(articles):
  if articles:
    df = pd.DataFrame(articles)
    try:
      existing_df = pd.read_csv(OUTPUT_FILE)
      df = pd.concat([existing_df, df], ignore_index=True)
    except FileNotFoundError:
      pass
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"💾 articles sheet created - {len(articles)} articles")

def get_articles_in_csv():
  try:
    df = pd.read_csv(OUTPUT_FILE)
    return len(df)
  except FileNotFoundError:
    return "⚠️ not found file to read the number of articles"

def config_proxy(pg):
  global PROXIES, USED_PROXIES
  while PROXIES:
    proxy = random.choice(PROXIES)
    if proxy not in USED_PROXIES:
      try:
        pg.SingleProxy(http=proxy, https=proxy)
        scholarly.use_proxy(pg)
        USED_PROXIES.add(proxy)
        print(f"🛜 proxy configured: {proxy}\n")
        return True
      except Exception as e:
        print(f"⚠️ error to configure proxy {proxy}: {e}")
        PROXIES.remove(proxy)
  print("0️⃣ no proxies available")
  return False

def get_free_proxies():
  urls = [
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
  ]
  proxies = []
  for url in urls:
    try:
      response = requests.get(url, timeout=5)
      if response.status_code == 200:
        new_proxies = response.text.splitlines()
        proxies.extend([proxy if proxy.startswith("http") else f"http://{proxy}" for proxy in new_proxies if proxy])
        print(f"⬇️ fetch {len(new_proxies)} proxies from {url}")
    except Exception as e:
      print(f"⚠️ erro to fetch proxies from {url}: {e}")
  return proxies if proxies else ["http://0.0.0.0:0000"]

PROXIES = []
USED_PROXIES = set()

if PROXY_TYPE != "NO_PROXY":
  pg = ProxyGenerator()
  if PROXY_TYPE == "GET_FREE_PROXY":
    PROXIES = get_free_proxies()
    config_proxy(pg)
  elif PROXY_TYPE == "LIB_FREE_PROXY":
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
    print("⚠️ invalid PROXY_TYPE, using LIB_FREE_PROXY type by default")
    pg.FreeProxies()
    print(f"🛜 lib proxy configured 'pg.FreeProxies()'")
  scholarly.use_proxy(pg)

try:
  print(f"🔍 searching articles...")
  search_results = scholarly.search_pubs(SEARCH_QUERY, year_low=INITIAL_SEARCH_YEAR, year_high=FINAL_SEARCH_YEAR)
except Exception as e:
  print(f"❌ error in articles search: {e}")
  exit(1)

articles = []
count_save_csv = 0
count_change_proxy = 0
total_articles = 0
print("🛠️ processing articles:")
try:
  for i, result in enumerate(search_results):
    total_articles += 1
    title = result['bib'].get('title', 'sem título')
    year = result['bib'].get('pub_year', 0)
    link_to_text = result.get('eprint_url', 'privado')
    link_to_local = result.get('pub_url', None)
    citations = result.get('num_citations', None)
    abstract = result['bib'].get('abstract', 'sem resumo')

    articles.append({
      'Nome do Artigo': title,
      'Ano': year,
      'Link público do texto': link_to_text,
      'Link do repositorio de busca': link_to_local,
      'Número de citações': citations,
      'Resumo': abstract,
      'Download': None
    })
    print(f'{i + 1}: {title} (Year: {year})')

    count_save_csv += 1
    count_change_proxy += 1
    if count_change_proxy >= CHANGE_PROXY_EVERY_N_ARTICLES:
      if PROXY_TYPE == "GET_FREE_PROXY":
        config_proxy(pg)
        count_change_proxy = 0
      elif PROXY_TYPE == "LIB_FREE_PROXY":
        print(f"🛜 lib proxy configuring...")
        pg.FreeProxies()
        scholarly.use_proxy(pg)
        print(f"🛜 lib proxy configured 'pg.FreeProxies()'")
        count_change_proxy = 0

    if count_save_csv >= SAVE_CSV_EVERY_N_ARTICLES:
      save_articles_csv(articles)
      count_save_csv = 0
      articles.clear()
      time.sleep(WAIT_TIME_PER_CSV_SAVE_SECONDS)
    else:
      time.sleep(WAIT_TIME_PER_ARTICLE_SEARCH_SECONDS)

    if STOP_IN_N_RESULTS > 0 and i >= STOP_IN_N_RESULTS - 1:
      print(f"🚦 stoping in {i + 1} results")
      break
except Exception as e:
  save_articles_csv(articles)
  print(f"❌ error in articles search: {e}")

if articles:
  save_articles_csv(articles)

print(f"\n📦 total articles processing: {total_articles}")
print(f"💾 total articles in csv: {get_articles_in_csv()}")
end_time = datetime.datetime.now()
total_time = end_time - start_time
print(f"⏱️ execution finished. Total time: {total_time}")
