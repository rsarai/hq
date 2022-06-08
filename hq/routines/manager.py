import json
import itertools
from typing import List

from dataclasses import dataclass

from hq.api import handler
from hq.modules import bash, habits, daylio, chrome, toggl, github, rescuetime, nubank, wakatime

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
    has_google_takeout_calendar: bool = False
    has_google_takeout_maps: bool = False
    has_google_takeout_my_activity: bool = False
    has_google_takeout_play_store: bool = False
    has_google_takeout_youtube: bool = False
    has_wakatime: bool = False
    state_file: str = '.db.json'
    working_files = []

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
            google takeout maps = {self.has_google_takeout_maps}
            google takeout myactivity = {self.has_google_takeout_my_activity}
            google takeout playstore = {self.has_google_takeout_play_store}
            google takeout youtube = {self.has_google_takeout_youtube}
            wakatime = {self.has_wakatime}
        """

    def fetch_memex_first_import(self):
        all_bash_files = all_habits_files = all_mood_files = all_browser_files = []
        all_toggl_files = all_rc_summary_files = all_rc_analytics_files = []
        all_gh_events_files = all_gh_notification_files = all_nubank_card_files = []
        all_nubank_account_files = all_nubank_bills_files = all_wakatime_files = []

        if self.has_bash:
            all_bash_files = bash.get_file_paths()
            bash_data_generator = bash.process(all_bash_files)
            yield from handler.process_bash(bash_data_generator)

        if self.has_habits:
            all_habits_files = habits.get_file_paths()
            habits_data_generator = habits.process(all_habits_files)
            yield from handler.process_habits(habits_data_generator)

        if self.has_daylio:
            all_mood_files = daylio.get_file_paths()
            daylio_data_generator = daylio.process(all_mood_files)
            yield from handler.process_moods(daylio_data_generator)

        if self.has_chrome:
            all_browser_files = chrome.get_file_paths()
            chrome_data_generator = chrome.process(all_browser_files)
            yield from handler.process_google_chrome(chrome_data_generator)

        if self.has_toggl:
            all_toggl_files = toggl.get_file_paths()
            toggl_data_generator = toggl.process(all_toggl_files)
            yield from handler.process_toggl(toggl_data_generator)

        if self.has_rescuetime:
            all_rc_summary_files = rescuetime.get_daily_summary_file_paths()
            rescuetime_data_generator = rescuetime.process_daily_summary(all_rc_summary_files)
            yield from handler.process_rescue_time_summary(rescuetime_data_generator)

            all_rc_analytics_files = rescuetime.get_analytic_data_file_paths()
            rescuetime_data_generator = rescuetime.process_analytic_data(all_rc_analytics_files)
            yield from handler.process_rescue_time_analytics(rescuetime_data_generator)

        if self.has_github:
            all_gh_events_files = github.get_events_file_paths()
            github_data_generator = github.process_events(all_gh_events_files)
            yield from handler.process_github_events(github_data_generator)

            all_gh_notification_files = github.get_notification_file_paths()
            github_data_generator = github.process_notifications(all_gh_notification_files)
            yield from handler.process_github_notifications(github_data_generator)

        if self.has_nubank:
            all_nubank_card_files = nubank.get_card_feed_files()
            nubank_data_generator = nubank.process_card_feed(all_nubank_card_files)
            yield from handler.process_nubank_card_feed(nubank_data_generator)

            all_nubank_account_files = nubank.get_account_feed_files()
            nubank_data_generator = nubank.process_account_feed(all_nubank_account_files)
            yield from handler.process_nubank_account_feed(nubank_data_generator)

            all_nubank_bills_files = nubank.get_bill_details_files()
            nubank_data_generator = nubank.process_bill_details(all_nubank_bills_files)
            yield from handler.process_nubank_bills(nubank_data_generator)

        if self.has_wakatime:
            all_wakatime_files = wakatime.get_file_paths()
            wakatime_data_generator = wakatime.process(all_wakatime_files)
            yield from handler.process_wakatime(wakatime_data_generator)

        self.working_files.extend([
            all_bash_files,
            all_habits_files,
            all_mood_files,
            all_browser_files,
            all_toggl_files,
            all_rc_summary_files,
            all_rc_analytics_files,
            all_gh_events_files,
            all_gh_notification_files,
            all_nubank_card_files,
            all_nubank_account_files,
            all_nubank_bills_files,
            all_wakatime_files,
        ])

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

    def fetch_updates(self):
        with open(self.state_file, 'r') as f:
            content = json.load(f)
        processed_files = content["processed_files"]

        all_bash_files = all_habits_files = all_mood_files = []
        all_browser_files = all_toggl_files = all_rc_summary_files = []
        all_rc_analytics_files = all_gh_events_files = all_gh_notification_files = []
        all_nubank_card_files = all_nubank_account_files = []
        all_nubank_bills_files = all_wakatime_files = []

        if self.has_bash:
            all_bash_files = [str(i) for i in bash.get_file_paths()]
            all_bash_files = set(all_bash_files) - set(processed_files)
            bash_data_generator = bash.process(all_bash_files)
            yield from handler.process_bash(bash_data_generator)

        if self.has_habits:
            all_habits_files = [str(i) for i in habits.get_file_paths()]
            all_habits_files = set(all_habits_files) - set(processed_files)
            habits_data_generator = habits.process(all_habits_files)
            yield from handler.process_habits(habits_data_generator)

        if self.has_daylio:
            all_mood_files = [str(i) for i in daylio.get_file_paths()]
            all_mood_files = set(all_mood_files) - set(processed_files)
            daylio_data_generator = daylio.process(all_mood_files)
            yield from handler.process_moods(daylio_data_generator)

        if self.has_chrome:
            all_browser_files = [str(i) for i in chrome.get_file_paths()]
            all_browser_files = set(all_browser_files) - set(processed_files)
            chrome_data_generator = chrome.process(all_browser_files)
            yield from handler.process_google_chrome(chrome_data_generator)

        if self.has_toggl:
            all_toggl_files = [str(i) for i in toggl.get_file_paths()]
            all_toggl_files = set(all_toggl_files) - set(processed_files)
            toggl_data_generator = toggl.process(all_toggl_files)
            yield from handler.process_toggl(toggl_data_generator)

        if self.has_rescuetime:
            all_rc_summary_files = [str(i) for i in rescuetime.get_daily_summary_file_paths()]
            all_rc_summary_files = set(all_rc_summary_files) - set(processed_files)
            rescuetime_data_generator = rescuetime.process_daily_summary(all_rc_summary_files)
            yield from handler.process_rescue_time_summary(rescuetime_data_generator)

            all_rc_analytics_files = [str(i) for i in rescuetime.get_analytic_data_file_paths()]
            all_rc_analytics_files = set(all_rc_analytics_files) - set(processed_files)
            rescuetime_data_generator = rescuetime.process_analytic_data(all_rc_analytics_files)
            yield from handler.process_rescue_time_analytics(rescuetime_data_generator)

        if self.has_github:
            all_gh_events_files = [str(i) for i in github.get_events_file_paths()]
            all_gh_events_files = set(all_gh_events_files) - set(processed_files)
            github_data_generator = github.process_events(all_gh_events_files)
            yield from handler.process_github_events(github_data_generator)

            all_gh_notification_files = [str(i) for i in github.get_notification_file_paths()]
            all_gh_notification_files = set(all_gh_notification_files) - set(processed_files)
            github_data_generator = github.process_notifications(all_gh_notification_files)
            yield from handler.process_github_notifications(github_data_generator)

        if self.has_nubank:
            all_nubank_card_files = [str(i) for i in nubank.get_card_feed_files()]
            all_nubank_card_files = set(all_nubank_card_files) - set(processed_files)
            nubank_data_generator = nubank.process_card_feed(all_nubank_card_files)
            yield from handler.process_nubank(nubank_data_generator)

            all_nubank_account_files = [str(i) for i in nubank.get_account_feed_files()]
            all_nubank_account_files = set(all_nubank_account_files) - set(processed_files)
            nubank_data_generator = nubank.process_account_feed(all_nubank_account_files)
            yield from handler.process_nubank_account_feed(nubank_data_generator)

            all_nubank_bills_files = [str(i) for i in nubank.get_bill_details_files()]
            all_nubank_bills_files = set(all_nubank_bills_files) - set(processed_files)
            nubank_data_generator = nubank.process_bill_details(all_nubank_bills_files)
            yield from handler.process_nubank_bills(nubank_data_generator)

        if self.has_wakatime:
            all_wakatime_files = [str(i) for i in wakatime.get_file_paths()]
            all_wakatime_files = set(all_wakatime_files) - set(processed_files)
            wakatime_data_generator = wakatime.process(all_wakatime_files)
            yield from handler.process_wakatime(wakatime_data_generator)

        self.working_files.extend([
            all_bash_files,
            all_habits_files,
            all_mood_files,
            all_browser_files,
            all_toggl_files,
            all_rc_summary_files,
            all_rc_analytics_files,
            all_gh_events_files,
            all_gh_notification_files,
            all_nubank_card_files,
            all_nubank_account_files,
            all_nubank_bills_files,
            all_wakatime_files,
        ])
