# Data Collection
Raw crossword data is scraped using scrape.py by making GET requests to https://www.nytimes.com/svc/crosswords/v6/puzzle/mini/{date}.json for all dates since the beginning of the mini crossword (2014-08-21) till 2024-11-12.

The raw data is then stored in data/raw/mini.

`python3 src/scrape.py https://www.nytimes.com/svc/crosswords/v6/puzzle/mini/ {cookie} {start_date} {end_date} {output_dir}`
