# **Google Scholar Article Search**

<p align="center"> 🚀 This script is designed to search articles in google scholar using specific search queries and configurations. It utilizes the `scholarly` library to perform the searches, scraper api and `pandas` to handle CSV operations. </p>

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

Python 3.12.0

Check libs and versions in [`requirements.txt`](requirements.txt)

To setup environment use (you will need [venv](https://docs.python.org/pt-br/3.13/library/venv.html)):

```
$ make setup
```

And enable the virtual ambient using:

```
$ source .venv/bin/activate
```

Ensure you have a `.env` file with the environment variable **SCRAPER_API_KEY**, you can get one in [scraper api](https://www.scraperapi.com/)

you can clean the environment using

```
$ make clean
```

<div id="using"></div>

## ☕ **Using**

First, check the [dependencies](#dependenciesandenvironment) and [install](#install) process

Here are the constants that control the application, you can edit them directly in the _main.py_ file:

- `WAIT_TIME_PER_ARTICLE_SEARCH_SECONDS`: Wait time (in seconds) between each article search.
- `WAIT_TIME_PER_CSV_SAVE_SECONDS`: Wait time (in seconds) between each CSV save.

- `SAVE_CSV_EVERY_N_ARTICLES`: Number of articles after which the CSV should be saved.
- `OUTPUT_FILE`: Name of the output CSV file.

- `STOP_IN_N_RESULTS`: Number of results after which the search should stop. Considered only if greater than 0.
- `INITIAL_SEARCH_YEAR`: Initial year for the article search.
- `FINAL_SEARCH_YEAR`: Final year for the article search.
- `SEARCH_QUERY`: variable to customize the search criteria.

Going to _root_ folder and exec:

```
$ python main.py
```

<div id="author"></div>

#### **👷 Author**

Made by Glener Pizzolato! 🙋

[![Linkedin Badge](https://img.shields.io/badge/-Glener-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/glener-pizzolato/)](https://www.linkedin.com/in/glener-pizzolato-6319821b0/)
[![Gmail Badge](https://img.shields.io/badge/-glenerpizzolato@gmail.com-c14438?style=flat-square&logo=Gmail&logoColor=white&link=mailto:glenerpizzolato@gmail.com)](mailto:glenerpizzolato@gmail.com)
