"""
this doesn't actually do much yet
"""
from collections import Counter
from pathlib import Path
import json
FEEDS_DIR = Path('data').joinpath('feeds')
datas = [json.loads(fpath.read_text()) for fpath in FEEDS_DIR.glob('*.json')]


c = Counter(d['status_code'] for d in datas)

print("Status code metrics:")
for k, v in c.most_common():
    print('{1}: {0}'.format(k, str(v).rjust(3)))

ys = [d for d in datas if d['status_code'] == 200]
xs = [d for d in ys if d['response_url'] != d['requested_url']]
print()
print("Of the {0} requests that were successful, {1} were likely redirects".format(len(ys), len(xs)))
