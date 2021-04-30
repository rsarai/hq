"""
format:
full_date,date,weekday,time,mood,activities,note_title,note
"""
import csv
import sys
import pytz

from datetime import datetime

sys.path.append('/home/sarai/github-projects/hq')
from hq.common import get_files
from hq.config import Daylio as config


timezone = pytz.timezone("America/Recife")


def get_file_path():
    """
        As of now, the export file has all the dataset history,
        so the processing of the latest file should be enough
    """
    return max(get_files(config.export_path, "*.csv"))


class Mood:
    def __init__(self, raw):
        self.raw = raw
        self.provider = "daylio"
        self.note = raw["note"]
        self.things_i_did = raw["activities"]
        self.mood = raw["mood"]

        full_date = raw["\ufefffull_date"]
        time = raw["time"]
        self.date_tz = datetime.strptime(
            full_date + "." + time,
            "%Y-%m-%d.%H:%M"
        ).replace(tzinfo=timezone)


def process():
    daylio_file = get_file_path()
    with open(daylio_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            yield Mood(row)
