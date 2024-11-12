import argparse
import os.path
from datetime import datetime

import grequests
import pandas as pd


def scrape_data(link_prefix, cookie, start_date, end_date, output_dir):
    reqs = []
    dates = pd.date_range(start=start_date, end=end_date).strftime("%Y-%m-%d")
    headers = {"cookie": cookie}
    for date in dates:
        link = f'{link_prefix}{date}.json'
        reqs.append(grequests.get(link, headers=headers))
    for date, resp in zip(dates, grequests.map(reqs)):
        if resp.status_code != 200:
            raise Exception('get request error: ' + str(resp.status_code), resp.reason)
        with open(os.path.join(output_dir, f'{date}.json'), 'wb') as file:
            file.write(resp.content)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Scrapes NYT mini crossword data within a specified date range and "
                                                 "stores the raw data in a specified output path")
    parser.add_argument("link_prefix", type=str, help="Link prefix")
    parser.add_argument("cookie", type=str, help="Cookie for given link prefix")
    parser.add_argument("start_date", type=str, help="Start date in YYYY-MM-DD format")
    parser.add_argument("end_date", type=str, help="End date in YYYY-MM-DD format")
    parser.add_argument("output_dir", type=str, help="Output path of raw data")
    args = parser.parse_args()
    try:
        datetime.strptime(args.start_date, "%Y-%m-%d")
        datetime.strptime(args.end_date, "%Y-%m-%d")
    except ValueError:
        parser.error("Dates should be in YYYY-MM-DD format")
    scrape_data(args.link_prefix, args.cookie, args.start_date, args.end_date, args.output_dir)
