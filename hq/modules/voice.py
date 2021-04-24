"""
Bookmarks from books and articles saved on @voice
"""
import os
import re
import sys
import json
import uuid
import pytz

from datetime import datetime, date

sys.path.append('/home/sarai/github-projects/hq')

from orger import pandoc

from hq.common import get_files
from hq.config import VoiceAudio as config


class Content:

    def __init__(self, raw, date):
        self.inputs = raw
        self.date = date
        self.bookmarks = []
        self.title = None
        self.process()

    def process(self):
        lines = self.inputs.split("\n\n")

        for line in lines:
            if '@Voice bookmarks exported' in line:
                self.title = self.process_title(line)
            elif '*** [' in line:
                continue
            else:
                self.bookmarks.append(line)

    def process_title(self, line):
        str_containing_title = line.split("/storage/1365-135E/Books/")[1]
        title = str_containing_title.split("\n")[0]
        return title


def process():
    voice_files = get_files(config.export_path, "*.txt")
    for f_path in voice_files:
        x = re.search("\d{4}-\d{2}-\d{2}", f_path.stem)
        date_str = x.group()

        if date_str:
            date = datetime.strptime(date_str,"%Y-%m-%d")
            if date.date() != date.today().date():
                continue

        yield Content(raw=f_path.read_text(), date=date)



if __name__ == "__main__":
    process()
