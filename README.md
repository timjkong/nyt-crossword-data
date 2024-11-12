# Project Background
NYT has published daily crosswords since 1993 and mini crosswords since 2014. The aim of this project is to train an LLM
to produce NYT-style crossword clues given input words. The project comprises data collection and model finetuning.

# Data Collection
## Scraping Raw Data
Raw mini data is scraped using scrape.py by making GET requests to 
https://www.nytimes.com/svc/crosswords/v6/puzzle/mini/{date}.json for all dates since the beginning of the mini 
crossword (2014-08-21) till 2024-11-12.

Similarly, raw crossword data is scraped via GET requests to 
https://www.nytimes.com/svc/crosswords/v6/puzzle/daily/{date}.json for all dates since the beginning (1993-11-24) till
2024-11-12

The raw mini/crossword data is then stored in data/raw/mini and data/raw/crossword respectively.

Run the following commands to scrape mini and crossword data:

`python3 src/scrape.py https://www.nytimes.com/svc/crosswords/v6/puzzle/mini/ {cookie} {start_date} {end_date} {output_dir}`

`python3 src/scrape.py https://www.nytimes.com/svc/crosswords/v6/puzzle/daily/ {cookie} {start_date} {end_date} {output_dir}`

## Data Processing
To train the model, the data should be in the format of word-to-clue pairs. More specifically, the processed data is 
stored in .jsonl format with "word" and "clue" as the keys.

During the processing, word-to-clue pairs that contain clues which reference other words in the same crossword were
removed from the dataset since they wouldn't make sense in isolation.

The cleaned data is stored in crossword-data.jsonl and mini-data.jsonl

## Data Size
crossword-data.jsonl contains 932391 word-to-clue pairs

mini-data.jsonl contains 39826 word-to-clue pairs 
