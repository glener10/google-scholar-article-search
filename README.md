# **Scholarly Article Search Script**

<p align="center"> 🚀 This script is designed to search for scholarly articles using specific search queries and configurations. It utilizes the `scholarly` library to perform the searches and `pandas` to handle CSV operations. </p>

<h3>🏁 Table of Contents</h3>

<br>

===================

<!--ts-->

💻 [Dependencies and Environment](#dependenciesandenvironment)

☕ [Using](#using)

👷 [Author](#author)

<!--te-->

===================

<div id="dependenciesandenvironment"></div>

## 💻 **Dependencies and Environment**

Dependencies and versions

- Python 3.10.12
- `scholarly` 1.7.11
- `requests` 2.25.1
- `pandas` 2.2.3

<div id="using"></div>

## ☕ **Using**

First, check the [dependencies](#dependenciesandenvironment) and the [installation](#installing) process

Here are the constants that control the application, you can edit them directly in the _main.py_ file:

- `WAIT_TIME_PER_ARTICLE_SEARCH_SECONDS`: Wait time (in seconds) between each article search.
- `WAIT_TIME_PER_CSV_SAVE_SECONDS`: Wait time (in seconds) between each CSV save.

- `PROXY_TYPE`: Type of proxy to be used. It can be `NO_PROXY`, `LIB_FREE_PROXY`, `GET_FREE_PROXY`, `SCRAPER_API` or `MANUAL`.

  - **`NO_PROXY`**:  
  No proxy will be used. The script will connect directly to the internet without routing requests through any proxy.

  - **`LIB_FREE_PROXY`**:  
  Uses a library of free proxies. The proxy list is provided by the `scholarly` package itself, and it will automatically switch between proxies to avoid being blocked or rate-limited.

  - **`GET_FREE_PROXY`**:  
  Retrieves a list of free proxies from external sources (such as websites with free proxy lists) and selects one randomly for each request. The proxy will change after a certain number of articles are processed, depending on the configuration.

  - **`SCRAPER_API (RECOMMENDED)`**:  
  Uses the ScraperAPI service to handle proxy management for web scraping. This service allows you to bypass restrictions by rotating proxies automatically and provides a paid solution for scraping.

  - **`MANUAL`**:  
  Allows you to manually specify the proxy. You need to provide the proxy details (e.g., IP address and port) in the environment variables. This option does not automatically rotate proxies and requires manual management.

- `CHANGE_PROXY_EVERY_N_ARTICLES`: Number of articles after which the proxy should be changed. Works only if `PROXY_TYPE` is `FREE_PROXY`.

- `SAVE_CSV_EVERY_N_ARTICLES`: Number of articles after which the CSV should be saved.
- `OUTPUT_FILE`: Name of the output CSV file.

- `STOP_IN_N_RESULTS`: Number of results after which the search should stop. Considered only if greater than 0.
- `INITIAL_SEARCH_YEAR`: Initial year for the article search.
- `FINAL_SEARCH_YEAR`: Final year for the article search.

- Ensure you have a `.env` file with the environment variable **SCRAPER_API_KEY** if using `SCRAPER_API` mode or **MANUAL_PROXY** if using `MANUAL` mode.

- Modify the `SEARCH_QUERY` variable to customize the search criteria.

Going to _root_ folder and exec:

```
$ python3 main.py
```

<div id="author"></div>

#### **👷 Author**

Made by Glener Pizzolato! 🙋

[![Linkedin Badge](https://img.shields.io/badge/-Glener-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/glener-pizzolato/)](https://www.linkedin.com/in/glener-pizzolato-6319821b0/)
[![Gmail Badge](https://img.shields.io/badge/-glenerpizzolato@gmail.com-c14438?style=flat-square&logo=Gmail&logoColor=white&link=mailto:glenerpizzolato@gmail.com)](mailto:glenerpizzolato@gmail.com)
