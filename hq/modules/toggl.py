import json
import pytz

from datetime import datetime
from pydantic import BaseModel
from typing import Optional

from hq.common import get_files, parse_datetime
from hq.config import Toggl as config


timezone = pytz.timezone("America/Recife")


TIME_DURATION_UNITS = (
    ('week', 60*60*24*7),
    ('day', 60*60*24),
    ('hour', 60*60),
    ('min', 60),
    ('sec', 1)
)


def human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'.format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)


def get_file_paths():
    return get_files(config.export_path, "*.json")


def get_projects_details_file():
    return max(get_files(config.export_path, "projects.json"))


def get_recent_file():
    return max(get_files(config.export_path, "*.json"))


class TimeEntry(BaseModel):
    raw: dict
    id: Optional[int]
    guid: Optional[str]
    start: Optional[datetime]
    stop: Optional[datetime]
    duration: Optional[int]
    human_time_duration: Optional[str]
    description: Optional[str]
    duronly: Optional[bool]
    tags: Optional[list]
    at: Optional[datetime]
    project_name: Optional[str]
    project_id: Optional[int]
    project_is_active: Optional[bool]

    def __init__(self, raw, projects) -> None:
        data = {"raw": raw}
        data["guid"] = raw["guid"]

        start = raw["start"]
        data["start"] = parse_datetime(start, '%Y-%m-%dT%H:%M:%S%z')

        stop = raw["stop"]
        data["stop"] = parse_datetime(stop, '%Y-%m-%dT%H:%M:%S%z')

        data["duration"] = raw["duration"]
        data["human_time_duration"] = human_time_duration(raw["duration"])
        data["description"] = raw.get("description")
        data["duronly"] = raw["duronly"]
        data["tags"] = raw.get("tags")

        at = raw["at"]
        data["at"] = parse_datetime(at, '%Y-%m-%dT%H:%M:%S%z')

        if raw.get("pid"):
            pid = raw["pid"]
            data["project_name"] = projects[pid].get("name")
            data["project_id"] = pid
            data["project_is_active"] = projects[pid].get("active")

        super().__init__(**data)


def _fetch_projects():
    file = get_projects_details_file()
    with open(file, 'r') as json_file:
        projects = {}
        content = json.load(json_file)
        for p in content:
            projects[p['id']] = p
    return projects


def process(input_files=None):
    if not input_files:
        input_files = get_file_paths()

    projects = _fetch_projects()
    handled = set()
    for file in input_files:
        if "projects.json" in str(file):
            continue

        with open(file, 'r') as json_file:
            content = json.load(json_file)
            for time_entry in content:
                guid = time_entry["guid"]
                if guid in handled:
                    continue
                else:
                    handled.add(guid)
                    yield TimeEntry(time_entry, projects)

