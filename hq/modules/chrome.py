"""
sources:
 - https://github.com/karlicoss/beepb00p-raw/blob/c8c301d23772ff60d45d6e3843a69e08ec521f99/unnecessary-db.org
 - https://gist.github.com/dropmeaword/9372cbeb29e8390521c2
 - https://web.archive.org/web/20200923160840/https://www.lowmanio.co.uk/blog/entries/how-google-chrome-stores-web-history/
"""
import pytz
import sqlite3

from datetime import datetime
from pydantic import BaseModel
from typing import Optional

from hq.common import get_files, parse_datetime
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

_ALTERNATIVE_QUERY = """
SELECT DISTINCT
    urls.url,
    urls.title,
    urls.visit_count,
    urls.typed_count,
    datetime(urls.last_visit_time/1000000-11644473600, "unixepoch") as last_visited,
    urls.hidden,
    datetime(visits.visit_time/1000000-11644473600, "unixepoch") as visit_time,
    visits.transition
FROM urls, visits
WHERE urls.id = visits.url
"""

KEYS = [
    "url", "title", "visit_count", "typed_count", "last_visited",
    "hidden", "visit_time", "transition", "publicly_routable",
]

ALTERNATIVE_KEYS = [
    "url", "title", "visit_count", "typed_count", "last_visited",
    "hidden", "visit_time", "transition"
]


timezone = pytz.timezone("America/Recife")


class Link(BaseModel):
    raw: dict
    url: Optional[str]
    title: Optional[str]
    visit_count: Optional[int]
    typed_count: Optional[int]
    hidden: Optional[int]
    transition: Optional[int]
    publicly_routable: Optional[int]
    date_tz: Optional[datetime]
    visit_time: Optional[datetime]

    def __init__(self, raw):
        data = {"raw": raw}

        data["url"] = raw["url"]
        data["title"] = raw["title"]
        data["visit_count"] = raw["visit_count"]
        data["typed_count"] = raw["typed_count"]
        data["hidden"] = raw["hidden"]
        data["transition"] = raw["transition"]
        data["publicly_routable"] = raw.get("publicly_routable")

        last_visited = raw["last_visited"]
        last_visited = parse_datetime(last_visited, '%Y-%m-%d %H:%M:%S')
        data["date_tz"] = last_visited

        visit_time = raw["visit_time"]
        visit_time = parse_datetime(visit_time, '%Y-%m-%d %H:%M:%S')
        data["visit_time"] = visit_time

        super().__init__(**data)


def get_file_paths():
    return list(get_files(config.export_path, glob='*.sqlite'))


def process(input_files=None):
    if not input_files:
        input_files = get_file_paths()

    handled = set()
    for db_path in input_files:
        with get_readonly_connection(db_path) as conn:
            cur = conn.cursor()
            try:
                cur.execute(_QUERY)
                _keys = KEYS
            except sqlite3.OperationalError:
                cur.execute(_ALTERNATIVE_QUERY)
                _keys = ALTERNATIVE_KEYS

            for row in cur.fetchall():
                res = dict(zip(_keys, row))

                visit_time = res["visit_time"]
                visit_time = parse_datetime(visit_time, '%Y-%m-%d %H:%M:%S')
                unique_set = f"""{res["last_visited"]}, {res["url"]}, {res["title"]}"""

                if unique_set in handled:
                    # ids are reseted and are not consisted through different devices
                    # uniqueness validation should be achieved by content
                    continue
                else:
                    handled.add(unique_set)
                    yield Link(res)
