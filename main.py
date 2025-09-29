import time
from scholarly import scholarly
from dotenv import load_dotenv
import datetime

from csv_operations import save_articles_csv, get_articles_in_csv
from proxy import config_proxy

start_time = datetime.datetime.now()
load_dotenv()

# 🕒 Wait time configurations
WAIT_TIME_PER_ARTICLE_SEARCH_SECONDS = 2
WAIT_TIME_PER_CSV_SAVE_SECONDS = 5

# 💾 CSV configurations
SAVE_CSV_EVERY_N_ARTICLES = 2
OUTPUT_FILE_NAME = "articles.csv"

# 🔎 Search configurations
STOP_IN_N_RESULTS = -1  # (only considered if is > 0)
INITIAL_SEARCH_YEAR = 2020
FINAL_SEARCH_YEAR = 2025
SEARCH_QUERY = '("security mechanisms" OR "protection mechanisms" OR "security measures" OR "security protocols" OR "fraud prevention") AND ("Brazilian instant payment" OR " instant payment system in Brazil" OR " PIX ") AND ("Brazil")'

print(f"🚀 Starting process at {start_time}")
print("🕒 Wait time configurations:")
print(
    f"  - Wait time per article search (seconds): {WAIT_TIME_PER_ARTICLE_SEARCH_SECONDS}"
)
print(f"  - Wait time per CSV save (seconds): {WAIT_TIME_PER_CSV_SAVE_SECONDS}")
print(f"💾 CSV configurations:")
print(f"  - Save CSV every N articles: {SAVE_CSV_EVERY_N_ARTICLES}")
print(f"  - Output file: {OUTPUT_FILE_NAME}")
print(f"🔎 Search configurations:")
if STOP_IN_N_RESULTS > 0:
    print(f"  - Stop in N results (only considered if is > 0): {STOP_IN_N_RESULTS}")
print(f"  - Year Range: {INITIAL_SEARCH_YEAR} to {FINAL_SEARCH_YEAR}")
print(f"  - Search Query: {SEARCH_QUERY}\n")

scholarly.use_proxy(config_proxy())

try:
    print(f"🔍 searching articles...")
    search_results = scholarly.search_pubs(
        SEARCH_QUERY, year_low=INITIAL_SEARCH_YEAR, year_high=FINAL_SEARCH_YEAR
    )
except Exception as e:
    print(f"❌ error in articles search: {e}")
    exit(1)

articles = []
count_save_csv = 0
total_articles = 0
print("🛠️ processing articles:")
try:
    for i, result in enumerate(search_results):
        total_articles += 1
        title = result["bib"].get("title", "sem título")
        year = result["bib"].get("pub_year", 0)
        link_to_text = result.get("eprint_url", "privado")
        link_to_local = result.get("pub_url", None)
        citations = result.get("num_citations", None)
        abstract = result["bib"].get("abstract", "sem resumo")

        articles.append(
            {
                "Nome do Artigo": title,
                "Ano": year,
                "Link público do texto": link_to_text,
                "Link do repositorio de busca": link_to_local,
                "Número de citações": citations,
                "Resumo": abstract,
                "Download": None,
            }
        )
        print(f"{i + 1}: {title} (Year: {year})")

        count_save_csv += 1
        if count_save_csv >= SAVE_CSV_EVERY_N_ARTICLES:
            save_articles_csv(articles, OUTPUT_FILE_NAME)
            count_save_csv = 0
            articles.clear()
            time.sleep(WAIT_TIME_PER_CSV_SAVE_SECONDS)
        else:
            time.sleep(WAIT_TIME_PER_ARTICLE_SEARCH_SECONDS)

        if STOP_IN_N_RESULTS > 0 and i >= STOP_IN_N_RESULTS - 1:
            print(f"🚦 stoping in {i + 1} results")
            break
except Exception as e:
    save_articles_csv(articles, OUTPUT_FILE_NAME)
    print(f"❌ error in articles search: {e}")

if articles:
    save_articles_csv(articles, OUTPUT_FILE_NAME)

print(f"\n📦 total articles processing: {total_articles}")
print(f"💾 total articles in csv: {get_articles_in_csv(OUTPUT_FILE_NAME)}")
end_time = datetime.datetime.now()
total_time = end_time - start_time
print(f"⏱️ execution finished. Total time: {total_time}")
