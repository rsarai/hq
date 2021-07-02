import json
import itertools

from dataclasses import dataclass

from hq.api import handler
from hq.modules import bash, habits, daylio, chrome, toggl, github, rescuetime, nubank

@dataclass
class ImportManager:
    has_bash: bool = True
    has_habits: bool = True
    has_daylio: bool = True
    has_chrome: bool = True
    has_toggl: bool = True
    has_github: bool = True
    has_rescuetime: bool = True
    has_nubank: bool = True
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
        """

    def fetch_memex_first_import(self):
        all_bash_files = []
        all_habits_files = []
        all_mood_files = []
        all_browser_files = []
        all_toggl_files = []
        all_rc_summary_files = []
        all_rc_analytics_files = []
        all_gh_events_files = []
        all_gh_notification_files = []
        all_nubank_files = []

        if self.has_bash:
            all_bash_files = bash.get_file_paths()
            yield from handler.process_bash(all_bash_files)

        if self.has_habits:
            all_habits_files = habits.get_file_paths()
            yield from handler.process_habits(all_habits_files)

        if self.has_daylio:
            all_mood_files = daylio.get_file_paths()
            yield from handler.process_moods(all_mood_files)

        if self.has_chrome:
            all_browser_files = chrome.get_file_paths()
            yield from handler.process_google_chrome(all_browser_files)

        if self.has_toggl:
            all_toggl_files = toggl.get_file_paths()
            yield from handler.process_toggl(all_toggl_files)

        if self.has_rescuetime:
            all_rc_summary_files = rescuetime.get_daily_summary_file_paths()
            yield from handler.process_rescue_time_summary(all_rc_summary_files)

            all_rc_analytics_files = rescuetime.get_analytic_data_file_paths()
            yield from handler.process_rescue_time_analytics(all_rc_analytics_files)

        if self.has_github:
            all_gh_events_files = github.get_events_file_paths()
            yield from handler.process_github_events(all_gh_events_files)

            all_gh_notification_files = github.get_notification_file_paths()
            yield from handler.process_github_notifications(all_gh_notification_files)

        if self.has_nubank:
            all_nubank_files = nubank.get_file_paths()
            yield from handler.process_nubank(all_nubank_files)

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
            all_nubank_files,
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

        all_bash_files = []
        all_habits_files = []
        all_mood_files = []
        all_browser_files = []
        all_toggl_files = []
        all_rc_summary_files = []
        all_rc_analytics_files = []
        all_gh_events_files = []
        all_gh_notification_files = []
        all_nubank_files = []

        if self.has_bash:
            all_bash_files = bash.get_file_paths()
            all_bash_files = set(all_bash_files) - set(processed_files)
            yield from handler.process_bash(all_bash_files)

        if self.has_habits:
            all_habits_files = habits.get_file_paths()
            all_habits_files = set(all_habits_files) - set(processed_files)
            yield from handler.process_habits(all_habits_files)

        if self.has_daylio:
            all_mood_files = daylio.get_file_paths()
            all_mood_files = set(all_mood_files) - set(processed_files)
            yield from handler.process_moods(all_mood_files)

        if self.has_chrome:
            all_browser_files = chrome.get_file_paths()
            all_browser_files = set(all_browser_files) - set(processed_files)
            yield from handler.process_google_chrome(all_browser_files)

        if self.has_toggl:
            all_toggl_files = toggl.get_file_paths()
            all_toggl_files = set(all_toggl_files) - set(processed_files)
            yield from handler.process_toggl(all_toggl_files)

        if self.has_rescuetime:
            all_rc_summary_files = rescuetime.get_daily_summary_file_paths()
            all_rc_summary_files = set(all_rc_summary_files) - set(processed_files)
            yield from handler.process_rescue_time_summary(all_rc_summary_files)

            all_rc_analytics_files = rescuetime.get_analytic_data_file_paths()
            all_rc_analytics_files = set(all_rc_analytics_files) - set(processed_files)
            yield from handler.process_rescue_time_analytics(all_rc_analytics_files)

        if self.has_github:
            all_gh_events_files = github.get_events_file_paths()
            all_gh_events_files = set(all_gh_events_files) - set(processed_files)
            yield from handler.process_github_events(all_gh_events_files)

            all_gh_notification_files = github.get_notification_file_paths()
            all_gh_notification_files = set(all_gh_notification_files) - set(processed_files)
            yield from handler.process_github_notifications(all_gh_notification_files)

        if self.has_nubank:
            all_nubank_files = nubank.get_file_paths()
            yield from handler.process_nubank(all_nubank_files)

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
            all_nubank_files,
        ])
