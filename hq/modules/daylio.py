"""
format:
full_date,date,weekday,time,mood,activities,note_title,note
"""
import csv
import pytz

from datetime import datetime
from pydantic import BaseModel
from typing import Optional

from hq.common import get_files, parse_datetime
from hq.config import Daylio as config


timezone = pytz.timezone("America/Recife")


def get_file_paths():
    """
        As of now, the export file has all the dataset history,
        so the processing of the latest file should be enough
    """
    return [max(get_files(config.export_path, "*.csv"))]


class Mood(BaseModel):
    raw: dict
    note: Optional[str] = None
    things_i_did: Optional[str] = None
    mood: Optional[str] = None
    date_tz: Optional[datetime] = None

    def __init__(self, raw):
        data = {"raw": raw}
        data["note"] = raw["note"]
        data["things_i_did"] = raw["activities"]
        data["mood"] = raw["mood"]

        full_date = raw["\ufefffull_date"]
        time = raw["time"]
        data["date_tz"] = parse_datetime(
            full_date + "." + time,
            "%Y-%m-%d.%H:%M"
        )

        super().__init__(**data)


def process(input_files=None):
    if not input_files:
        input_files = get_file_paths()

    for daylio_file in input_files:
        with open(daylio_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                yield Mood(row)
