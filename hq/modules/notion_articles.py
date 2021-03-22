"""
Good Saved Articles from Notion
"""
import os
import re
import sys
import json
import uuid
import pytz

from datetime import datetime

sys.path.append('/home/sarai/github-projects/hq')

from orger import pandoc

from hq.common import get_files
from hq.config import NotionArticles as config


class Article:

    def __init__(self, raw, images_folder):
        self.raw = raw
        self.images_folder = images_folder

    @property
    def uuid(self):
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, self.title()))

    def title(self):
        p = self.raw.split('\n')[0]
        return p.replace("* ", '').strip()

    def datetime(self):
        p = re.search(r'(?:(((Jan(uary)?|Ma(r(ch)?|y)|Jul(y)?|Aug(ust)?|Oct(ober)?|Dec(ember)?)\ 31)|((Jan(uary)?|Ma(r(ch)?|y)|Apr(il)?|Ju((ly?)|(ne?))|Aug(ust)?|Oct(ober)?|(Sept|Nov|Dec)(ember)?)\ (0?[1-9]|([12]\d)|30))|(Feb(ruary)?\ (0?[1-9]|1\d|2[0-8]|(29(?=,\ ((1[6-9]|[2-9]\d)(0[48]|[2468][048]|[13579][26])|((16|[2468][048]|[3579][26])00)))))))\,\ ((1[6-9]|[2-9]\d)\d{2}))', self.raw)
        dt = datetime.strptime(p.group(), '%b %d, %Y')
        return pytz.utc.localize(dt)


def md_to_org(raw):
    org = pandoc.to_org(raw, from_='markdown')
    org = org.replace('Column: ', '\nDate :: ')
    org = org.replace(' URL: ', '\nURL :: ')
    return org


def process():
    notion_files = get_files(config.export_path, "*.md")

    for f_path in notion_files:
        images_folder = None
        if f_path.stem in notion_files:
            images_folder = f"{f_path.parent.absolute()}/{f_path.stem}"

        yield Article(
            raw=md_to_org(f_path.read_text()),
            images_folder=images_folder,
        )



if __name__ == "__main__":
    # from hq import settings
    process()

