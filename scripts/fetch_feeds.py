from collections import OrderedDict
from deco import *
from datetime import datetime
from pathlib import Path
from re import sub
from urllib.parse import urlparse
import csv
import json
import requests
DATA_DIR = Path('data')
CSV_PATH = DATA_DIR.joinpath('rss-urls.csv')
FEEDS_DIR = DATA_DIR.joinpath('feeds')
FEEDS_DIR.mkdir(parents=True, exist_ok=True)

@concurrent
def fetch_feed(url):
    d = OrderedDict()
    d['requested_url'] = url
    d['fetched_at'] = datetime.now().isoformat()
    print("Downloading", url)
    try:
        resp = requests.get(url, allow_redirects=True)
    except Exception as err:
        d['status_code'] = err.__class__.__name__
        d['response_text'] = str(err)
        d['headers'] = None
    else:
        d['status_code'] = resp.status_code
        d['response_text'] = resp.text
        d['headers'] = dict(resp.headers)
        d['response_url'] = resp.url
    finally:
        u = urlparse(url)
        fn = u.netloc + '---' + u.path[1:] + '__' + u.query
        fpath = FEEDS_DIR.joinpath(sub(r'[^\w\.\-]+', '_', fn).strip('_') + '.json')
        with fpath.open('w') as f:
            json.dump(d, f, indent=2)
            print("Status code: {0}; Wrote to: {1}".format(d['status_code'], fpath))

@synchronized
def main():
    for line in csv.DictReader(CSV_PATH.open('r')):
        url = line['rss-url']
        fetch_feed(url)


if __name__ == '__main__':
    main()
