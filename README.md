# Carver

[![CI](https://github.com/dddjjjbbb/Lish/actions/workflows/python-app.yml/badge.svg)](https://github.com/dddjjjbbb/Lish/actions/workflows/python-app.yml)
[![License: GPL-3.0](https://img.shields.io/badge/License-GPL--3.0-blue.svg)](LICENSE)

<img src="logo.png" alt="Project Logo" width="300"/>

Want to pull reams of data for a large collection of books? Carver has you covered.
With speed and accuracy, Carver aims to facilitate the generation of large data sets without use of the Goodreads API.

# TOC

1. [How to install](#how-to-install)
2. [How to use](#how-to-use)
   - [Config](#config)
   - [Tests](#tests)
3. [Services](#services)
   1. [Collect Book Metadata](#collect-book-metadata)
   2. [Collect Book Reviews](#collect-book-reviews)
   3. [Generate Book Id Titles](#generate-book-id-titles)
4. [Schema Gate](#schema-gate)
5. [Technologies used](#technologies-used)
6. [Glossary](#glossary)
7. [Acknowledgements](#acknowledgements)
8. [Notes](#notes)

# How to install

You'll need [Python 3.10+](https://www.python.org/downloads/).

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The review service also requires a web browser (Chrome or Firefox).
Firefox tends to work better.

# How to use

We recommend running these services from the command line, as the usage instructions below describe.

## Config

Many defaults can be configured via the project `config.ini`.

You'll currently find fields related to book/author metadata.

Under `[BOOK]` or `[AUTHOR]`, mark fields as either `True` or `False` and corresponding limits as desired.

e.g. if you're not interested in exporting the genres to which a book belongs, change `GENRES = True` to `GENRES = False`

## Tests

Run tests with `python -m pytest tests/ --cov=src/` from root.

Smoke tests that hit live Goodreads are in `tests/smoke/` and excluded from the main suite.
To run them manually:

```bash
python -m pytest tests/smoke/ -v
```

# Collect Book Metadata

You can use the below commands to collect metadata about books on Goodreads,
such as the total number of Goodreads reviews and ratings, average Goodreads rating,
and most common Goodreads "shelves" for each book.

### Input

This service takes as input a list of book id titles, stored in a plain text file with one book id title per line.
Book id titles are unique to Goodreads and can be found at the end of a book's URL.
For example, the book id title for *Little Women*
([https://www.goodreads.com/book/show/1934.Little_Women](https://www.goodreads.com/book/show/1934.Little_Women))
is `1934.Little_Women`.

Note: If you don't have these ids to hand but only a list of books/authors, Carver can automate the process for you,
see: [Generate Book Ids](#generate-book-id-titles)

### Output

The service outputs a JSON file for each book with the information marked as `True` under `[BOOK]` in `config.ini`.
By default, all values listed will be included in the output.

This service also outputs an aggregated JSON file with information about all the books that have been scraped.
To output an aggregated CSV file in addition to a JSON file, use the flag `--format CSV`.

### Usage

```bash
python main.py -s book -bip example/data/goodreads_classics_sample.txt -odp user_io/output/ -f csv
```

# Collect Book Reviews

You can use the review service to collect reviews and review metadata about books on Goodreads,
including the text of the review, star rating, username of the reviewer, number of likes,
and categories or "shelves" that the user has tagged for the book.

### Input

This service takes as input a list of book IDs, stored in a plain text file with one book ID per line.

### Output

This service outputs a JSON file for each book with the following information:

- book ID and title
- review URL
- review ID
- date
- rating
- username of the reviewer
- text
- number of likes the review received from other users
- shelves to which the reviewer added the book

To output an aggregated CSV file in addition to a JSON file, use the flag `--format csv`.

Goodreads only allows the first 10 pages of reviews to be shown for each book.
There are 30 reviews per page, so you should expect a maximum of 300 reviews per book.

By default, the reviews are sorted by their popularity.

They can also be sorted chronologically to show either the newest or oldest reviews.

- `sort_order` can be set to `default`, `newest` or `oldest`.

We also select a filter to only show English language reviews.

### Usage

```bash
python src/review/review_service.py --book_ids_path example/data/goodreads_classics_sample.txt --output_directory_path . --browser firefox --sort_order newest --format json
```

- `browser` can be set to `chrome` or `firefox`.
- `format` can be set to `JSON` (default) or `CSV`.

# Generate Book Id Titles

You can use the service `book_id` to collect book id titles which can then be used as input to any of the above services.

### Input

This service takes as input a list of queries stored as plain text with one `book_title - book_author` per line.
The default location of this file is `user_io/input/goodreads_queries.txt`.
The delimiter can be whatever you wish, but it must be specified in the config file: `config.ini` (the default is " - ").

### Output

For matches, this service outputs a book id title for each book here `user_io/output/matches/matches.txt`.
For no matches, the service outputs the original query here `user_io/output/no_matches/no_matches.txt`.

### Usage

```bash
python main.py -s book_id
```

Should you wish to change the match percentages or output paths, you can do so in the `config.ini`.

Percentages are currently set as follows:

```
BOOK_TITLE_SIMILARITY_PERCENTAGE = 0.6
AUTHOR_NAME_SIMILARITY_PERCENTAGE = 0.7
```

We found these to be sane defaults during testing, but it really will depend on your use case, feel free to experiment :)

# Schema Gate

Goodreads periodically changes its HTML structure, which can silently break the scraper.
Carver guards against this with a **schema gate**: a set of smoke tests that validate every CSS selector
and regex pattern the scraper depends on against a live Goodreads page.

### How it works

- `schema/expected_selectors.json` defines the contract: every selector and pattern the scraper uses.
- `tests/smoke/test_schema_gate.py` fetches a live book page and checks that each selector still finds elements.
- A GitHub Actions workflow (`.github/workflows/schema-gate.yml`) runs these tests weekly on Monday mornings.
- If any selector fails, the workflow automatically opens a GitHub issue with the `schema-drift` label, detailing exactly which selectors broke.

### When the gate fires

1. Visit the test URL in a browser and inspect the elements that failed.
2. Update the selectors in `src/book/book_service.py`.
3. Update `schema/expected_selectors.json` to match the new selectors.
4. Update test fixtures in `tests/unit/src/book/data/`.

### Running manually

```bash
python -m pytest tests/smoke/test_schema_gate.py -v
```

The workflow can also be triggered manually from the GitHub Actions tab.

# Technologies Used

- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)
- [Selenium](https://selenium-python.readthedocs.io/installation.html)
- [aiohttp](https://docs.aiohttp.org/) (async HTTP for list/shelf scraping)
- [SPARQLWrapper](https://sparqlwrapper.readthedocs.io/) (Wikidata queries for author metadata)
- [pandas](https://pandas.pydata.org/) (CSV export)

# Glossary

- `book_id_title` corresponds to the id contained in the goodreads URL,
  e.g. `587393.The_Lost_Scrapbook` in `https://www.goodreads.com/book/show/587393.The_Lost_Scrapbook`
- `numeric_book_id` corresponds to the numeric section of the book_id_title,
  e.g. `587393` in `587393.The_Lost_Scrapbook`

# Acknowledgements

Carver is a fork of the excellent `goodreads-scraper` project
started by [Maria Antoniak](https://github.com/maria-antoniak) and [Melanie Walsh](https://github.com/melaniewalsh).

It was motivated by moving that project forward given time constraints on the part of the original owners.
Plus the vision/intention is slightly different. For a list of changes/motivation see:
[changes](./changes.md)

The original project has since been declared unmaintained by its authors, so Carver has been detached
from the fork and now continues as a standalone project.

I am indebted to them for their initial efforts and thank them for helping to get this project off the ground.
For full details of the original project, please see [the repo](https://github.com/maria-antoniak/goodreads-scraper).

# Notes

- Updates to the Goodreads website may break this code.
  The [schema gate](#schema-gate) will detect most breakages automatically,
  but we don't guarantee that Carver will continue to work in the future.
  Feel free to post an issue if you run into a problem.

- The review service has received the least refactoring attention and is the most fragile.

The code is licensed under a GNU General Public License v3.0.
