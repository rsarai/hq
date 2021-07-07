import sys
import json
import pytz

from typing import Optional
from datetime import datetime
from pydantic import BaseModel

sys.path.append('/home/sarai/github-projects/hq')
from hq.common import get_files, parse_datetime
from hq.config import RescueTime as config


timezone = pytz.timezone("America/Recife")


def get_daily_summary_file_paths():
    return get_files(config.export_path + "/daily_summary/", "*.json")


def get_analytic_data_file_paths():
    return get_files(config.export_path + "/analytic_data/", "*.json")


class Report(BaseModel):
    raw: dict
    date_tz: Optional[datetime]
    productivity_pulse: Optional[int]
    very_productive_percentage: Optional[float]
    productive_percentage: Optional[float]
    neutral_percentage: Optional[float]
    distracting_percentage: Optional[float]
    very_distracting_percentage: Optional[float]
    all_productive_percentage: Optional[float]
    all_distracting_percentage: Optional[float]
    uncategorized_percentage: Optional[float]
    business_percentage: Optional[float]
    communication_and_scheduling_percentage: Optional[float]
    social_networking_percentage: Optional[float]
    design_and_composition_percentage: Optional[float]
    entertainment_percentage: Optional[float]
    news_percentage: Optional[float]
    software_development_percentage: Optional[float]
    reference_and_learning_percentage: Optional[float]
    shopping_percentage: Optional[float]
    utilities_percentage: Optional[float]
    total_hours: Optional[float]
    very_productive_hours: Optional[float]
    productive_hours: Optional[float]
    neutral_hours: Optional[float]
    distracting_hours: Optional[float]
    very_distracting_hours: Optional[float]
    all_productive_hours: Optional[float]
    all_distracting_hours: Optional[float]
    uncategorized_hours: Optional[float]
    business_hours: Optional[float]
    communication_and_scheduling_hours: Optional[float]
    social_networking_hours: Optional[float]
    design_and_composition_hours: Optional[float]
    entertainment_hours: Optional[float]
    news_hours: Optional[float]
    software_development_hours: Optional[float]
    reference_and_learning_hours: Optional[float]
    shopping_hours: Optional[float]
    utilities_hours: Optional[float]
    total_duration_formatted: Optional[str]
    very_productive_duration_formatted: Optional[str]
    productive_duration_formatted: Optional[str]
    neutral_duration_formatted: Optional[str]
    distracting_duration_formatted: Optional[str]
    very_distracting_duration_formatted: Optional[str]
    all_productive_duration_formatted: Optional[str]
    all_distracting_duration_formatted: Optional[str]
    uncategorized_duration_formatted: Optional[str]
    business_duration_formatted: Optional[str]
    communication_and_scheduling_duration_formatted: Optional[str]
    social_networking_duration_formatted: Optional[str]
    design_and_composition_duration_formatted: Optional[str]
    entertainment_duration_formatted: Optional[str]
    news_duration_formatted: Optional[str]
    software_development_duration_formatted: Optional[str]
    reference_and_learning_duration_formatted: Optional[str]
    shopping_duration_formatted: Optional[str]
    utilities_duration_formatted: Optional[str]

    def __init__(self, raw) -> None:
        data = {"raw": raw}
        date = raw["date"]
        date = parse_datetime(date, '%Y-%m-%d')
        date_tz = date.replace(hour=23, minute=59)
        data["date_tz"] = date_tz

        data["productivity_pulse"] = raw["productivity_pulse"]
        data["very_productive_percentage"] = raw["very_productive_percentage"]
        data["productive_percentage"] = raw["productive_percentage"]
        data["neutral_percentage"] = raw["neutral_percentage"]
        data["distracting_percentage"] = raw["distracting_percentage"]
        data["very_distracting_percentage"] = raw["very_distracting_percentage"]
        data["all_productive_percentage"] = raw["all_productive_percentage"]
        data["all_distracting_percentage"] = raw["all_distracting_percentage"]
        data["uncategorized_percentage"] = raw["uncategorized_percentage"]
        data["business_percentage"] = raw["business_percentage"]
        data["communication_and_scheduling_percentage"] = raw["communication_and_scheduling_percentage"]
        data["social_networking_percentage"] = raw["social_networking_percentage"]
        data["design_and_composition_percentage"] = raw["design_and_composition_percentage"]
        data["entertainment_percentage"] = raw["entertainment_percentage"]
        data["news_percentage"] = raw["news_percentage"]
        data["software_development_percentage"] = raw["software_development_percentage"]
        data["reference_and_learning_percentage"] = raw["reference_and_learning_percentage"]
        data["shopping_percentage"] = raw["shopping_percentage"]
        data["utilities_percentage"] = raw["utilities_percentage"]
        data["total_hours"] = raw["total_hours"]
        data["very_productive_hours"] = raw["very_productive_hours"]
        data["productive_hours"] = raw["productive_hours"]
        data["neutral_hours"] = raw["neutral_hours"]
        data["distracting_hours"] = raw["distracting_hours"]
        data["very_distracting_hours"] = raw["very_distracting_hours"]
        data["all_productive_hours"] = raw["all_productive_hours"]
        data["all_distracting_hours"] = raw["all_distracting_hours"]
        data["uncategorized_hours"] = raw["uncategorized_hours"]
        data["business_hours"] = raw["business_hours"]
        data["communication_and_scheduling_hours"] = raw["communication_and_scheduling_hours"]
        data["social_networking_hours"] = raw["social_networking_hours"]
        data["design_and_composition_hours"] = raw["design_and_composition_hours"]
        data["entertainment_hours"] = raw["entertainment_hours"]
        data["news_hours"] = raw["news_hours"]
        data["software_development_hours"] = raw["software_development_hours"]
        data["reference_and_learning_hours"] = raw["reference_and_learning_hours"]
        data["shopping_hours"] = raw["shopping_hours"]
        data["utilities_hours"] = raw["utilities_hours"]
        data["total_duration_formatted"] = raw["total_duration_formatted"]
        data["very_productive_duration_formatted"] = raw["very_productive_duration_formatted"]
        data["productive_duration_formatted"] = raw["productive_duration_formatted"]
        data["neutral_duration_formatted"] = raw["neutral_duration_formatted"]
        data["distracting_duration_formatted"] = raw["distracting_duration_formatted"]
        data["very_distracting_duration_formatted"] = raw["very_distracting_duration_formatted"]
        data["all_productive_duration_formatted"] = raw["all_productive_duration_formatted"]
        data["all_distracting_duration_formatted"] = raw["all_distracting_duration_formatted"]
        data["uncategorized_duration_formatted"] = raw["uncategorized_duration_formatted"]
        data["business_duration_formatted"] = raw["business_duration_formatted"]
        data["communication_and_scheduling_duration_formatted"] = raw["communication_and_scheduling_duration_formatted"]
        data["social_networking_duration_formatted"] = raw["social_networking_duration_formatted"]
        data["design_and_composition_duration_formatted"] = raw["design_and_composition_duration_formatted"]
        data["entertainment_duration_formatted"] = raw["entertainment_duration_formatted"]
        data["news_duration_formatted"] = raw["news_duration_formatted"]
        data["software_development_duration_formatted"] = raw["software_development_duration_formatted"]
        data["reference_and_learning_duration_formatted"] = raw["reference_and_learning_duration_formatted"]
        data["shopping_duration_formatted"] = raw["shopping_duration_formatted"]
        data["utilities_duration_formatted"] = raw["utilities_duration_formatted"]

        super().__init__(**data)


class Entry(BaseModel):
    raw: list
    date_tz: Optional[datetime]
    time_spent_in_seconds: Optional[int]
    number_of_people: Optional[int]
    detail: Optional[str]
    category: Optional[str]
    productivity: Optional[int]

    def __init__(self, raw) -> None:
        data = {"raw": raw}

        date = raw[0]
        date = parse_datetime(date, '%Y-%m-%dT%H:%M:%S')
        date_tz = date.replace(hour=23, minute=59)
        data["date_tz"] = date_tz
        data["time_spent_in_seconds"] = raw[1]
        data["number_of_people"] = raw[2]
        data["detail"] = raw[3]
        data["category"] = raw[4]
        data["productivity"] = raw[5]

        super().__init__(**data)


def process_analytic_data(input_files=None):
    if not input_files:
        input_files = get_analytic_data_file_paths()

    handled = set()
    for file in input_files:
        with open(file, 'r') as json_file:
            content = json.load(json_file)
            for raw in content['rows']:
                uniq_id = f"{raw[0]} {raw[1]} {raw[3]}"
                if uniq_id in handled:
                    continue
                else:
                    handled.add(uniq_id)
                    yield Entry(raw)


def process_daily_summary(input_files=None):
    if not input_files:
        input_files = get_daily_summary_file_paths()

    handled = set()
    for file in input_files:
        with open(file, 'r') as json_file:
            content = json.load(json_file)
            for summary in content:
                id = summary["id"]
                if id in handled:
                    continue
                else:
                    handled.add(id)
                    yield Report(summary)
