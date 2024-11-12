import argparse
import json
from datetime import datetime

import grequests
import pandas as pd

LINK_PREFIX = 'https://www.nytimes.com/svc/crosswords/v6/puzzle/mini/'
HEADERS = {
    "accept": "*/*",
    "accept-language": "en-GB,en;q=0.9",
    "content-type": "application/x-www-form-urlencoded",
    "cookie": "nyt-a=7_W5W5Kbj-8VkhbUEZ88_4; purr-cache=<G_<C_<T0<Tp1_<Tp2_<Tp3_<Tp4_<Tp7_<a0_<K0<S0<r<ur; nyt-auth-method=sso; nyt-b3-traceid=e7338ccd77684a858688a5e6ccdacc44; SIDNY=CBkSMQiEr7y5BhCE-sy5BhoSMS1Hc7roeT5hw8seWpZSQzBTINaf9m0qAgACONOb8K4GQgAaQOuz4aq8avjmJ_fB3MJfjy-oGRl6yY32aDne1y2w97WgVPGbUVGtZm6Y_RLz624YiTOVPddurA9VVzI5ApN7KQI=; NYT-S=0^CBkSMQiEr7y5BhCE-sy5BhoSMS1Hc7roeT5hw8seWpZSQzBTINaf9m0qAgACONOb8K4GQgAaQOuz4aq8avjmJ_fB3MJfjy-oGRl6yY32aDne1y2w97WgVPGbUVGtZm6Y_RLz624YiTOVPddurA9VVzI5ApN7KQI=; nyt-gdpr=0; nyt-geo=SG; nyt-jkidd=uid=230526934&lastRequest=1731411089095&activeDays=%5B0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C1%2C0%2C0%2C1%5D&adv=2&a7dv=2&a14dv=2&a21dv=2&lastKnownType=sub&newsStartDate=&entitlements=XWD; nyt-purr=cfhhcfhhhckfhcfshgas2; _dd_s=rum=0&expire=1731411996108",
    "dnt": "1",
    "priority": "u=1, i",
    "referer": "https://www.nytimes.com/crosswords/game/mini/2024/10/05",
    "sec-ch-ua": "\"Not;A=Brand\";v=\"24\", \"Chromium\";v=\"128\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "x-games-auth-bypass": "true"
}


def scrape_data(start_date, end_date, output_path):
    reqs = []
    dates = pd.date_range(start=start_date, end=end_date).strftime("%Y-%m-%d")
    for date in dates:
        link = f'{LINK_PREFIX}{date}.json'
        reqs.append(grequests.get(link, headers=HEADERS))
    output_data = []
    for date, resp in zip(dates, grequests.map(reqs)):
        if resp.status_code != 200:
            raise Exception('get request error: ' + str(resp.status_code), resp.reason)
        output_data.extend(format_data(resp.content))
    jsonl_data = '\n'.join(json.dumps(entry) for entry in output_data) + '\n'
    with open(output_path, 'w') as output_file:
        output_file.write(jsonl_data)


def format_data(json_str):
    data = json.loads(json_str)["body"][0]
    cells = data["cells"]
    clues = [clue["text"][0]["plain"] for clue in data["clues"]]
    words = [[] for _ in range(len(clues))]
    for cell in cells:
        if "clues" not in cell:
            continue
        for i in cell["clues"]:
            words[i].append(cell["answer"])
    output_data = [{
        "word": ''.join(word).lower(),
        "clue": clue.lower()
    } for word, clue in zip(words, clues)]
    return output_data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Scrapes NYT mini crossword mini-data within a specified date range")
    parser.add_argument("output_path", type=str, help="Output path of jsonl mini-data")
    parser.add_argument("start_date", type=str, help="Start date in YYYY-MM-DD format")
    parser.add_argument("end_date", type=str, help="End date in YYYY-MM-DD format")
    args = parser.parse_args()
    if not args.output_path.endswith('.jsonl'):
        parser.error("output_path should be a path to a .jsonl file")
    try:
        datetime.strptime(args.start_date, "%Y-%m-%d")
        datetime.strptime(args.end_date, "%Y-%m-%d")
    except ValueError:
        parser.error("Dates should be in YYYY-MM-DD format")
    scrape_data(args.start_date, args.end_date, args.output_path)
