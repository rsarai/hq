import json
import itertools
from typing import List

from dataclasses import dataclass, field

from hq.api import handler
from hq.modules import (
    bash, habits, daylio, chrome, toggl, github, rescuetime, nubank, wakatime,
)
from hq.modules.google_takeout import (
    calendar as google_takeout_calendar,
    maps as google_takeout_maps,
    my_activity as google_takeout_activity,
    play_store as google_takeout_play_store,
)

@dataclass
class ImportManager:
    has_bash: bool = True
    has_chrome: bool = True
    has_daylio: bool = True
    has_github: bool = True
    has_habits: bool = True
    has_toggl: bool = True
    has_rescuetime: bool = True
    has_nubank: bool = True
    has_google_takeout_calendar: bool = True
    has_google_takeout_maps_semantic: bool = True
    has_google_takeout_my_activity: bool = True
    has_google_takeout_play_store: bool = True
    has_google_takeout_youtube: bool = False
    has_wakatime: bool = True
    state_file: str = '.db_v2.json'
    working_files: List = field(default_factory=list)

    @classmethod
    def available_providers(cls):
        return [
            {"label": "Bash", "value": "bash"},
            {"label": "Habits", "value": "habits"},
            {"label": "Daylio", "value": "daylio"},
            {"label": "Chrome", "value": "google chrome"},
            {"label": "Toggl", "value": "toggl"},
            {"label": "Github", "value": "github"},
            {"label": "Rescuetime", "value": "rescuetime"},
            {"label": "Nubank", "value": "nubank"},
            {"label": "Google takeout calendar", "value": "google takeout calendar"},
            {"label": "Google takeout maps", "value": "google takeout maps"},
            {"label": "Google takeout my activity", "value": "google takeout my activity"},
            {"label": "Play store", "value": "play store"},
            {"label": "Wakatime", "value": "wakatime"},
        ]

    def available_importers(self):
        return f"""
            bash = {self.has_bash}
            habits = {self.has_habits}
            daylio = {self.has_daylio}
            chrome = {self.has_chrome}
            toggl = {self.has_toggl}
            github = {self.has_github}
            rescuetime = {self.has_rescuetime}
            nubank = {self.has_nubank}
            google takeout calendar = {self.has_google_takeout_calendar}
            google takeout maps = {self.has_google_takeout_maps_semantic}
            google takeout myactivity = {self.has_google_takeout_my_activity}
            google takeout playstore = {self.has_google_takeout_play_store}
            google takeout youtube = {self.has_google_takeout_youtube}
            wakatime = {self.has_wakatime}
        """

    def _process_bash(self, bash_file_paths):
        bash_data_generator = bash.process(bash_file_paths)
        yield from handler.process_bash(bash_data_generator)

    def _process_habits(self, file_paths):
        habits_data_generator = habits.process(file_paths)
        yield from handler.process_habits(habits_data_generator)

    def _process_daylio(self, file_paths):
        daylio_data_generator = daylio.process(file_paths)
        yield from handler.process_moods(daylio_data_generator)

    def _process_chrome(self, file_paths):
        chrome_data_generator = chrome.process(file_paths)
        yield from handler.process_google_chrome(chrome_data_generator)

    def _process_toggl(self, file_paths):
        toggl_data_generator = toggl.process(file_paths)
        yield from handler.process_toggl(toggl_data_generator)

    def _process_rescue_time_summary(self, file_paths):
        rescuetime_data_generator = rescuetime.process_daily_summary(file_paths)
        yield from handler.process_rescue_time_summary(rescuetime_data_generator)

    def _process_rescue_time_analytics(self, file_paths):
        rescuetime_data_generator = rescuetime.process_analytic_data(file_paths)
        yield from handler.process_rescue_time_analytics(rescuetime_data_generator)

    def _process_github_events(self, file_paths):
        github_data_generator = github.process_events(file_paths)
        yield from handler.process_github_events(github_data_generator)

    def _process_github_notifications(self, file_paths):
        github_data_generator = github.process_notifications(file_paths)
        yield from handler.process_github_notifications(github_data_generator)

    def _process_nubank_card_feed(self, file_paths):
        nubank_data_generator = nubank.process_card_feed(file_paths)
        yield from handler.process_nubank_card_feed(nubank_data_generator)

    def _process_nubank_account_feed(self, file_paths):
        nubank_data_generator = nubank.process_account_feed(file_paths)
        yield from handler.process_nubank_account_feed(nubank_data_generator)

    def _process_nubank_bills(self, file_paths):
        nubank_data_generator = nubank.process_bill_details(file_paths)
        yield from handler.process_nubank_bills(nubank_data_generator)

    def _process_wakatime(self, file_paths):
        wakatime_data_generator = wakatime.process(file_paths)
        yield from handler.process_wakatime(wakatime_data_generator)

    def _process_google_takeout_calendar(self, file_paths):
        google_takeout_calendar_generator = google_takeout_calendar.process_my_calendars(file_paths)
        yield from handler.process_google_takeout_calendar(google_takeout_calendar_generator)

    def _process_google_takeout_maps_semantic_locations(self, file_paths):
        google_takeout_maps_generator = google_takeout_maps.process_semantic_locations(
            file_paths
        )
        yield from handler.process_google_takeout_maps_semantic_locations(
            google_takeout_maps_generator
        )

    def _process_google_takeout_my_activity(self, file_paths):
        gt_activity_generator = google_takeout_activity.process_my_activities(
            file_paths
        )
        yield from handler.process_google_takeout_my_activity(gt_activity_generator)

    def _process_google_takeout_play_store(self, file_paths):
        gt_play_store_generator = google_takeout_play_store.process(file_paths)
        yield from handler.process_google_takeout_play_store(gt_play_store_generator)

    def fetch_memex_first_import(self):
        files_dict = {
            "all_bash_files": bash.get_file_paths(),
            "all_habits_files": habits.get_file_paths(),
            "all_mood_files": daylio.get_file_paths(),
            "all_browser_files": chrome.get_file_paths(),
            "all_toggl_files": toggl.get_file_paths(),
            "all_rc_summary_files": rescuetime.get_daily_summary_file_paths(),
            "all_rc_analytics_files": rescuetime.get_analytic_data_file_paths(),
            "all_gh_events_files": github.get_events_file_paths(),
            "all_gh_notification_files": github.get_notification_file_paths(),
            "all_nubank_card_files": nubank.get_card_feed_files(),
            "all_nubank_account_files": nubank.get_account_feed_files(),
            "all_nubank_bills_files": nubank.get_bill_details_files(),
            "all_wakatime_files": wakatime.get_file_paths(),
            "all_google_takeout_calendar": google_takeout_calendar.get_file_paths(),
            "all_google_takeout_maps_files": google_takeout_maps.get_file_paths(),
            "all_google_takeout_my_activity_files": google_takeout_activity.get_my_activities_file_paths(),
            "all_gt_play_store_files": google_takeout_play_store.get_file_paths(),
        }

        yield from self.process_providers_by_files(files_dict)
        for key_files in files_dict.values():
            self.working_files.extend([key_files])

    def fetch_updates(self):
        with open(self.state_file, 'r') as f:
            content = json.load(f)
        processed_files = content["processed_files"]

        files_dict = {}
        all_bash_files = [str(i) for i in bash.get_file_paths()]
        all_bash_files = set(all_bash_files) - set(processed_files)
        files_dict["all_bash_files"] = all_bash_files

        all_habits_files = [str(i) for i in habits.get_file_paths()]
        all_habits_files = set(all_habits_files) - set(processed_files)
        files_dict["all_habits_files"] = all_habits_files

        all_mood_files = [str(i) for i in daylio.get_file_paths()]
        all_mood_files = set(all_mood_files) - set(processed_files)
        files_dict["all_mood_files"] = all_mood_files

        all_browser_files = [str(i) for i in chrome.get_file_paths()]
        all_browser_files = set(all_browser_files) - set(processed_files)
        files_dict["all_browser_files"] = all_browser_files

        all_toggl_files = [str(i) for i in toggl.get_file_paths()]
        all_toggl_files = set(all_toggl_files) - set(processed_files)
        files_dict["all_toggl_files"] = all_toggl_files

        all_rc_summary_files = [str(i) for i in rescuetime.get_daily_summary_file_paths()]
        all_rc_summary_files = set(all_rc_summary_files) - set(processed_files)
        files_dict["all_rc_summary_files"] = all_rc_summary_files

        all_rc_analytics_files = [str(i) for i in rescuetime.get_analytic_data_file_paths()]
        all_rc_analytics_files = set(all_rc_analytics_files) - set(processed_files)
        files_dict["all_rc_analytics_files"] = all_rc_analytics_files

        all_gh_events_files = [str(i) for i in github.get_events_file_paths()]
        all_gh_events_files = set(all_gh_events_files) - set(processed_files)
        files_dict["all_gh_events_files"] = all_gh_events_files

        all_gh_notification_files = [str(i) for i in github.get_notification_file_paths()]
        all_gh_notification_files = set(all_gh_notification_files) - set(processed_files)
        files_dict["all_gh_notification_files"] = all_gh_notification_files

        all_nubank_card_files = [str(i) for i in nubank.get_card_feed_files()]
        all_nubank_card_files = set(all_nubank_card_files) - set(processed_files)
        files_dict["all_nubank_card_files"] = all_nubank_card_files

        all_nubank_account_files = [str(i) for i in nubank.get_account_feed_files()]
        all_nubank_account_files = set(all_nubank_account_files) - set(processed_files)
        files_dict["all_nubank_account_files"] = all_nubank_account_files

        all_nubank_bills_files = [str(i) for i in nubank.get_bill_details_files()]
        all_nubank_bills_files = set(all_nubank_bills_files) - set(processed_files)
        files_dict["all_nubank_bills_files"] = all_nubank_bills_files

        all_wakatime_files = [str(i) for i in wakatime.get_file_paths()]
        all_wakatime_files = set(all_wakatime_files) - set(processed_files)
        files_dict["all_wakatime_files"] = all_wakatime_files

        all_google_takeout_calendar = [str(i) for i in google_takeout_calendar.get_file_paths()]
        all_google_takeout_calendar = set(all_google_takeout_calendar) - set(processed_files)
        files_dict["all_google_takeout_calendar"] = all_google_takeout_calendar

        all_google_takeout_maps_files = [str(i) for i in google_takeout_maps.get_file_paths()]
        all_google_takeout_maps_files = set(all_google_takeout_maps_files) - set(processed_files)
        files_dict["all_google_takeout_maps_files"] = all_google_takeout_maps_files

        all_google_takeout_my_activity_files = [str(i) for i in google_takeout_activity.get_my_activities_file_paths()]
        all_google_takeout_my_activity_files = set(all_google_takeout_my_activity_files) - set(processed_files)
        files_dict["all_google_takeout_my_activity_files"] = all_google_takeout_my_activity_files

        all_gt_play_store_files = [str(i) for i in google_takeout_play_store.get_file_paths()]
        all_gt_play_store_files = set(all_gt_play_store_files) - set(processed_files)
        files_dict["all_gt_play_store_files"] = all_gt_play_store_files

        yield from self.process_providers_by_files(files_dict)
        for key_files in files_dict.values():
            self.working_files.extend([key_files])

    def mark_import_as_completed(self):
        assert self.working_files != []

        with open(self.state_file, 'w') as f:
            flat = list(itertools.chain(*self.working_files))
            data = {"processed_files": list(set([str(f) for f in flat]))}
            json.dump(data, f)

    def reset(self):
        with open(self.state_file, 'w') as f:
            data = {"processed_files": []}
            json.dump(data, f)

    def process_providers_by_files(self, files_dict):
        if self.has_bash:
            yield from self._process_bash(files_dict["all_bash_files"])

        if self.has_habits:
            yield from self._process_habits(files_dict["all_habits_files"])

        if self.has_daylio:
            yield from self._process_daylio(files_dict["all_mood_files"])

        if self.has_chrome:
            yield from self._process_chrome(files_dict["all_browser_files"])

        if self.has_toggl:
            yield from self._process_toggl(files_dict["all_toggl_files"])

        if self.has_rescuetime:
            yield from self._process_rescue_time_summary(files_dict["all_rc_summary_files"])
            yield from self._process_rescue_time_analytics(files_dict["all_rc_analytics_files"])

        if self.has_github:
            yield from self._process_github_events(files_dict["all_gh_events_files"])
            yield from self._process_github_notifications(files_dict["all_gh_notification_files"])

        if self.has_nubank:
            yield from self._process_nubank_card_feed(files_dict["all_nubank_card_files"])
            yield from self._process_nubank_account_feed(files_dict["all_nubank_account_files"])
            yield from self._process_nubank_bills(files_dict["all_nubank_bills_files"])

        if self.has_wakatime:
            yield from self._process_wakatime(files_dict["all_wakatime_files"])

        if self.has_google_takeout_calendar:
            yield from self._process_google_takeout_calendar(files_dict["all_google_takeout_calendar"])

        if self.has_google_takeout_maps_semantic:
            yield from self._process_google_takeout_maps_semantic_locations(
                files_dict["all_google_takeout_maps_files"]
            )

        if self.has_google_takeout_my_activity:
            yield from self._process_google_takeout_my_activity(
                files_dict["all_google_takeout_my_activity_files"]
            )

        if self.has_google_takeout_play_store:
            yield from self._process_google_takeout_play_store(
                files_dict["all_gt_play_store_files"]
            )
