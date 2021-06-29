import sys
import json
import pytz

from datetime import datetime

sys.path.append('/home/sarai/github-projects/hq')
from hq.common import get_files
from hq.config import Toggl as config


timezone = pytz.timezone("America/Recife")


def get_file_paths():
    return get_files(config.export_path, "*.json")


def get_projects_details_file():
    return max(get_files(config.export_path, "projects.json"))


def get_recent_file():
    return max(get_files(config.export_path, "*.json"))


class TimeEntry:
    def __init__(self, raw, projects) -> None:
        self.raw = raw
        self.id = raw["id"]
        self.guid = raw["guid"]

        self.start = raw["start"]
        self.start = datetime.strptime(self.start, '%Y-%m-%dT%H:%M:%S%z')
        self.start = self.start.astimezone(timezone)

        self.stop = raw["stop"]
        self.stop = datetime.strptime(self.stop, '%Y-%m-%dT%H:%M:%S%z')
        self.stop = self.start.astimezone(timezone)

        self.duration = raw["duration"]
        self.description = raw.get("description")
        self.duronly = raw["duronly"]

        self.tags = raw.get("tags")

        self.at = raw["at"]
        self.at = datetime.strptime(self.at, '%Y-%m-%dT%H:%M:%S%z')

        self.project_name = None
        self.project_id = None
        self.project_is_active = None
        if raw.get("pid"):
            pid = raw["pid"]
            self.project_name = projects[pid].get("name")
            self.project_id = pid
            self.project_is_active = projects[pid].get("active")


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

