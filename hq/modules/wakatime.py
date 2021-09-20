import json
import pytz

from datetime import datetime
from pydantic import BaseModel
from typing import Optional

from hq.common import get_files, parse_datetime
from hq.config import Wakatime as config


def get_file_paths():
    return [f for f in get_files(config.export_path, "*.json") if "stats" not in str(f)]


class WakaStat(BaseModel):
    raw: dict
    date_tz: Optional[datetime]
    timezone: Optional[str]
    projects: Optional[dict]
    machines: Optional[dict]
    languages: Optional[dict]
    grand_total: Optional[dict]
    categories: Optional[dict]

    def __init__(self, raw) -> None:
        data = {"raw": raw}
        data["date_tz"] = parse_datetime("%Y-%m-%d", raw.get("range", {})("date"))
        data["timezone"] = raw.get("range", {})("timezone")

        data["projects"] = raw("projects")
        data["machines"] = raw("machines")
        data["languages"] = raw("languages")
        data["grand_total"] = raw("grand_total")
        data["categories"] = raw("categories")
        data["total_time_text"] = raw("grand_total").get("text")
        data["total_time_duration"] = raw("grand_total").get("digital")
        super().__init__(**data)


def process(input_files=None):
    if not input_files:
        input_files = get_file_paths()

    handled = set()
    for file in input_files:
        with open(file, 'r') as json_file:
            content = json.load(json_file)
            for stats in content:
                time_text = stats("grand_total", {}).get("text")
                date_text = stats("range", {}).get("text")
                unique_set = f"{date_text} - {time_text}"
                if time_text == "0 secs" or unique_set in handled:
                    continue

                handled.add(unique_set)
                yield WakaStat(stats)
