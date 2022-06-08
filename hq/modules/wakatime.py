import json
import pytz

from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

from hq.common import get_files, parse_datetime
from hq.config import Wakatime as config


def get_file_paths():
    return [f for f in get_files(config.export_path, "*.json") if "stats" not in str(f)]


class WakaStat(BaseModel):
    raw: dict
    date_tz: Optional[datetime]
    timezone: Optional[str]
    projects: List[dict]
    machines: List[dict]
    languages: List[dict]
    grand_total: Optional[dict]
    categories: List[dict]

    def __init__(self, raw) -> None:
        data = {"raw": raw}

        date_str = raw.get("range", {}).get("date")
        data["date_tz"] = parse_datetime(date_str, "%Y-%m-%d")
        data["timezone"] = raw.get("range", {}).get("timezone")

        data["projects"] = raw.get("projects")
        data["machines"] = raw.get("machines")
        data["languages"] = raw.get("languages")
        data["grand_total"] = raw.get("grand_total")
        data["categories"] = raw.get("categories")
        data["total_time_text"] = raw.get("grand_total").get("text")
        data["total_time_duration"] = raw.get("grand_total").get("digital")
        super().__init__(**data)


def process(input_files=None):
    if not input_files:
        input_files = get_file_paths()

    handled = set()
    for file in input_files:
        with open(file, 'r') as json_file:
            content = json.load(json_file)
            for stats in content:
                time_text = stats.get("grand_total", {}).get("text")
                date_text = stats.get("range", {}).get("text")
                unique_set = f"{date_text} - {time_text}"
                if time_text == "0 secs" or unique_set in handled:
                    continue

                handled.add(unique_set)
                yield WakaStat(stats)
