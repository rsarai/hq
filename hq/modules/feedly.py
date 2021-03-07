"""
Feedly RSS reader
"""
import pytz
import json

from datetime import datetime

from hq.common import get_files
from hq.config import Feedly as config


def parse_file(f):
    raw = json.loads(f)
    import ipdb; ipdb.set_trace()
    for r in raw:
        rid = r['id']
        website = r.get('website', rid)
        # yield Subscription(
        #     created_at=None,
        #     title=r['title'],
        #     url=website,
        #     id=rid,
        # )

def process():
    feedly_files = get_files(config.export_path)
    for f in feedly_files:
        subs = parse_file(f)
        dts = f.stem.split('_')[-1]
        dt = datetime.strptime(dts, '%Y%m%d%H%M%S')
        dt = pytz.utc.localize(dt)
        # yield dt, subs
