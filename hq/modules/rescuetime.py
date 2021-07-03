import sys
import json
import pytz

from datetime import datetime

sys.path.append('/home/sarai/github-projects/hq')
from hq.common import get_files
from hq.config import RescueTime as config


timezone = pytz.timezone("America/Recife")


def get_daily_summary_file_paths():
    return get_files(config.export_path + "/daily_summary/", "*.json")


def get_analytic_data_file_paths():
    return get_files(config.export_path + "/analytic_data/", "*.json")


class Report:

    def __init__(self, raw) -> None:
        self.raw = raw
        self.date = raw["date"]
        self.date = datetime.strptime(self.date, '%Y-%m-%d')
        self.datetime = self.date.replace(hour=23, minute=59)
        self.datetime = self.datetime.astimezone(timezone)

        self.productivity_pulse = raw["productivity_pulse"]
        self.very_productive_percentage = raw["very_productive_percentage"]
        self.productive_percentage = raw["productive_percentage"]
        self.neutral_percentage = raw["neutral_percentage"]
        self.distracting_percentage = raw["distracting_percentage"]
        self.very_distracting_percentage = raw["very_distracting_percentage"]
        self.all_productive_percentage = raw["all_productive_percentage"]
        self.all_distracting_percentage = raw["all_distracting_percentage"]
        self.uncategorized_percentage = raw["uncategorized_percentage"]
        self.business_percentage = raw["business_percentage"]
        self.communication_and_scheduling_percentage = raw["communication_and_scheduling_percentage"]
        self.social_networking_percentage = raw["social_networking_percentage"]
        self.design_and_composition_percentage = raw["design_and_composition_percentage"]
        self.entertainment_percentage = raw["entertainment_percentage"]
        self.news_percentage = raw["news_percentage"]
        self.software_development_percentage = raw["software_development_percentage"]
        self.reference_and_learning_percentage = raw["reference_and_learning_percentage"]
        self.shopping_percentage = raw["shopping_percentage"]
        self.utilities_percentage = raw["utilities_percentage"]
        self.total_hours = raw["total_hours"]
        self.very_productive_hours = raw["very_productive_hours"]
        self.productive_hours = raw["productive_hours"]
        self.neutral_hours = raw["neutral_hours"]
        self.distracting_hours = raw["distracting_hours"]
        self.very_distracting_hours = raw["very_distracting_hours"]
        self.all_productive_hours = raw["all_productive_hours"]
        self.all_distracting_hours = raw["all_distracting_hours"]
        self.uncategorized_hours = raw["uncategorized_hours"]
        self.business_hours = raw["business_hours"]
        self.communication_and_scheduling_hours = raw["communication_and_scheduling_hours"]
        self.social_networking_hours = raw["social_networking_hours"]
        self.design_and_composition_hours = raw["design_and_composition_hours"]
        self.entertainment_hours = raw["entertainment_hours"]
        self.news_hours = raw["news_hours"]
        self.software_development_hours = raw["software_development_hours"]
        self.reference_and_learning_hours = raw["reference_and_learning_hours"]
        self.shopping_hours = raw["shopping_hours"]
        self.utilities_hours = raw["utilities_hours"]
        self.total_duration_formatted = raw["total_duration_formatted"]
        self.very_productive_duration_formatted = raw["very_productive_duration_formatted"]
        self.productive_duration_formatted = raw["productive_duration_formatted"]
        self.neutral_duration_formatted = raw["neutral_duration_formatted"]
        self.distracting_duration_formatted = raw["distracting_duration_formatted"]
        self.very_distracting_duration_formatted = raw["very_distracting_duration_formatted"]
        self.all_productive_duration_formatted = raw["all_productive_duration_formatted"]
        self.all_distracting_duration_formatted = raw["all_distracting_duration_formatted"]
        self.uncategorized_duration_formatted = raw["uncategorized_duration_formatted"]
        self.business_duration_formatted = raw["business_duration_formatted"]
        self.communication_and_scheduling_duration_formatted = raw["communication_and_scheduling_duration_formatted"]
        self.social_networking_duration_formatted = raw["social_networking_duration_formatted"]
        self.design_and_composition_duration_formatted = raw["design_and_composition_duration_formatted"]
        self.entertainment_duration_formatted = raw["entertainment_duration_formatted"]
        self.news_duration_formatted = raw["news_duration_formatted"]
        self.software_development_duration_formatted = raw["software_development_duration_formatted"]
        self.reference_and_learning_duration_formatted = raw["reference_and_learning_duration_formatted"]
        self.shopping_duration_formatted = raw["shopping_duration_formatted"]
        self.utilities_duration_formatted = raw["utilities_duration_formatted"]


class Entry:

    def __init__(self, raw) -> None:
        self.raw = raw
        self.date = raw[0]
        self.date = datetime.strptime(self.date, '%Y-%m-%dT%H:%M:%S')
        self.datetime = self.date.replace(hour=23, minute=59)
        self.datetime = self.datetime.astimezone(timezone)

        self.time_spent_in_seconds = raw[1]
        self.number_of_people = raw[2]
        self.detail = raw[3]
        self.category = raw[4]
        self.productivity = raw[5]


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
