"""
sources:
 - https://github.com/karlicoss/beepb00p-raw/blob/c8c301d23772ff60d45d6e3843a69e08ec521f99/unnecessary-db.org
 - https://gist.github.com/dropmeaword/9372cbeb29e8390521c2
 - https://web.archive.org/web/20200923160840/https://www.lowmanio.co.uk/blog/entries/how-google-chrome-stores-web-history/
"""

import sys
import pytz
from datetime import datetime

sys.path.append('/home/sarai/github-projects/hq')

from hq.common import get_files
from hq.sqlite_db import get_readonly_connection
from hq.config import ChromeHistory as config


_QUERY = """
SELECT DISTINCT
    urls.url,
    urls.title,
    urls.visit_count,
    urls.typed_count,
    datetime(urls.last_visit_time/1000000-11644473600, "unixepoch") as last_visited,
    urls.hidden,
    datetime(visits.visit_time/1000000-11644473600, "unixepoch") as visit_time,
    visits.transition,
    visits.publicly_routable
FROM urls, visits
WHERE urls.id = visits.url
"""

KEYS = [
    "url", "title", "visit_count", "typed_count", "last_visited",
    "hidden", "visit_time", "transition", "publicly_routable",
]


timezone = pytz.timezone("America/Recife")


class Link:
    def __init__(self, raw):
        self.raw = raw

        self.provider = "google chrome"
        self.url = raw["url"]
        self.title = raw["title"]
        self.visit_count = raw["visit_count"]
        self.typed_count = raw["typed_count"]
        self.hidden = raw["hidden"]
        self.transition = raw["transition"]
        self.publicly_routable = raw["publicly_routable"]

        last_visited = raw["last_visited"]
        last_visited = datetime.strptime(last_visited, '%Y-%m-%d %H:%M:%S')
        self.date_tz = timezone.localize(last_visited)

        visit_time = raw["visit_time"]
        visit_time = datetime.strptime(visit_time, '%Y-%m-%d %H:%M:%S')
        self.visit_time = timezone.localize(visit_time)


def get_file_paths():
    return list(get_files(config.export_path, glob='*.sqlite'))


def process():
    handled = set()
    chrome_databases = get_file_paths()

    for db_path in chrome_databases:
        with get_readonly_connection(db_path) as conn:
            cur = conn.cursor()
            cur.execute(_QUERY)
            for row in cur.fetchall():
                res = dict(zip(KEYS, row))
                unique_set = f"""{res["visit_time"]}, {res["last_visited"]}, {res["url"]}, {res["title"]}"""
                if unique_set in handled:
                    # ids are reseted and are not consisted through different devices
                    # uniqueness validation should be achieved by content
                    continue
                else:
                    handled.add(unique_set)
                    yield Link(res)
