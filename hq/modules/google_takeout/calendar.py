import pytz
import zipfile

from pydantic import BaseModel
from typing import Optional, Any, Set
from datetime import datetime, timezone

from hq.common import get_files
from hq.config import GoogleTakeout as config

from ics import Calendar


timezone = pytz.timezone("America/Recife")


def get_file_paths():
    files = []
    files.append(max(get_files(config.export_path, "vinta*")))
    files.append(max(get_files(config.export_path, "ecomp*")))
    files.append(max(get_files(config.export_path, "takeout*")))
    return files


class Event(BaseModel):
    raw: Optional[dict]
    duration: Optional[str] = None
    end_time: Optional[datetime]
    begin: Optional[datetime]
    begin_precision: Optional[str]
    status: Optional[str]
    classification: Optional[str] = None
    organizer: Optional[str] = None
    uid: Optional[str]
    description: Optional[str]
    created: Optional[datetime]
    last_modified: Optional[datetime]
    location: Optional[str] = ''
    url: Optional[str] = None
    transparent: Optional[bool] = False
    alarms: Optional[list] = []
    attendees: Optional[Set] = set()
    categories: Optional[Set] = set()
    geo: Optional[str] = None
    name: Optional[str]
    tz: Optional[Any]


    def __init__(__pydantic_self__, **data: Any) -> None:
        raw = data.pop("raw")

        data["duration"] = raw._duration
        data["begin_precision"] = raw._begin_precision
        data["status"] = raw._status
        data["classification"] = raw._classification
        data["uid"] = raw.uid
        data["description"] = raw.description

        if raw.organizer:
            data["organizer"] = str(raw.organizer).split("=")[1]

        if raw._classmethod_kwargs['tz'].get('America/Recife'):
            tz = raw._classmethod_kwargs['tz']['America/Recife']
            tz = pytz.timezone(tz._tzid)
        else:
            tz = timezone

        data["tz"] = tz
        if hasattr(raw, '_end_data'):
            data["end_data"] = raw._end_data.astimezone(tz)
        data["begin"] = raw._begin.astimezone(tz)
        data["created"] = raw.created.astimezone(tz)
        data["last_modified"] = raw.last_modified.astimezone(tz)

        data["location"] = raw.location
        data["url"] = raw.url
        data["transparent"] = raw.transparent
        data["alarms"] = raw.alarms
        data["attendees"] = raw.attendees
        data["categories"] = raw.categories
        data["geo"] = raw.geo
        data["name"] = raw.name

        print(data.get('organizer'))
        super().__init__(**data)


def process_my_calendars(input_files=None):
    if not input_files:
        input_files = get_file_paths()

    for zip_path in input_files:
        zf = zipfile.ZipFile(zip_path)
        my_calendar_files = [
            f.filename for f in zf.filelist if f.filename.endswith(".ics")
        ]

        for file_name in my_calendar_files:
            with zf.open(file_name) as f:
                ics_content = f.read()
                c = Calendar(ics_content.decode("utf-8"))

                for event in c.events:
                    yield Event(raw=event)
