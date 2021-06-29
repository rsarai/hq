import sys
import json
import pytz

from datetime import datetime

sys.path.append('/home/sarai/github-projects/hq')
from hq.common import get_files
from hq.config import Github as config


timezone = pytz.timezone("America/Recife")


def get_events_file_paths():
    return get_files(config.export_path + "/events/", "*.json")


def get_notification_file_paths():
    return get_files(config.export_path + "/notifications/", "*[!_details].json")


def get_notification_detail_file_paths():
    return get_files(config.export_path + "/notifications/", "*_details.json")


class Notification:

    def __init__(self, raw, details) -> None:
        self.raw = raw
        self.github_id = raw["id"]
        self.reason = raw["reason"]
        self.repository = {
            "id": raw.get("repository", {}).get("id"),
            "name": raw.get("repository", {}).get("name"),
            "full_name": raw.get("repository", {}).get("full_name"),
            "private": raw.get("repository", {}).get("private"),
            "description": raw.get("repository", {}).get("description"),
            "url": raw.get("repository", {}).get("html_url"),
        }
        self.url = raw["url"]
        self.updated_at_str = raw["updated_at"]
        self.updated_at = datetime.strptime(self.updated_at_str, '%Y-%m-%dT%H:%M:%S%z')
        self.updated_at = self.updated_at.astimezone(timezone)

        if details:
            key = self.github_id + self.updated_at_str

            if details.get(key):
                original = raw["subject"].copy()
                original.update(details[key])
                self.subject = original
            else:
                self.subject = raw["subject"]
        else:
            self.subject = raw["subject"]


class Event:

    def __init__(self, raw) -> None:
        self.raw = raw
        self.github_id = raw["id"]
        self.type = raw["type"]
        self.actor = raw["actor"].get("login")
        self.public = raw["public"]
        self.created_at = raw["created_at"]
        self.created_at = datetime.strptime(self.created_at, '%Y-%m-%dT%H:%M:%S%z')
        self.created_at = self.created_at.astimezone(timezone)
        self.repo = {
            "id": raw.get("repo", {}).get("id"),
            "name": raw.get("repo", {}).get("name"),
            "url": raw.get("repo", {}).get("url"),
        }

        self.org = None
        if raw.get("org"):
            self.org = raw["org"].get("login")

        self.create_data = None
        self.delete_data = None
        self.issue_comment_data = None
        self.pull_request_data = None
        self.pull_request_review_comment_data = None
        self.pull_request_review_event_data = None
        self.push_data = None
        self.watch_data = None

        if self.type == "CreateEvent":
            self.create_data = {
                "ref": raw["payload"]["ref"],
                "ref_type": raw["payload"]["ref_type"],
                "master_branch": raw["payload"]["master_branch"],
                "description": raw["payload"]["description"],
            }
        elif self.type == "DeleteEvent":
            self.delete_data = {
                "ref": raw["payload"]["ref"],
                "ref_type": raw["payload"]["ref_type"],
                "pusher_type": raw["payload"]["pusher_type"],
            }
        elif self.type == "IssueCommentEvent":
            created_at = raw["payload"]["issue"]["created_at"]
            if created_at:
                created_at = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%S%z')
                created_at = created_at.astimezone(timezone)

            updated_at = raw["payload"]["issue"]["updated_at"]
            if updated_at:
                updated_at = datetime.strptime(updated_at, '%Y-%m-%dT%H:%M:%S%z')
                updated_at = updated_at.astimezone(timezone)

            closed_at = raw["payload"]["issue"]["closed_at"]
            if closed_at:
                closed_at = datetime.strptime(closed_at, '%Y-%m-%dT%H:%M:%S%z')
                closed_at = closed_at.astimezone(timezone)

            assignee = raw["payload"]["issue"]["assignee"]
            self.issue_comment_data = {
                "action": raw["payload"]["action"],
                "issue": {
                    "number": raw["payload"]["issue"]["number"],
                    "title": raw["payload"]["issue"]["title"],
                    "user": raw["payload"]["issue"]["user"]["login"],
                    "labels": raw["payload"]["issue"]["labels"],
                    "state": raw["payload"]["issue"]["state"],
                    "assignee": assignee.get("user", {}).get("login") if assignee else assignee,
                    "assignees": [
                        user.get("login")
                        for user in raw["payload"]["issue"]["assignees"] if user
                    ],
                    "comments": raw["payload"]["issue"]["comments"],
                    "created_at": created_at,
                    "updated_at": updated_at,
                    "closed_at": closed_at,
                    "author_association": raw["payload"]["issue"]["author_association"],
                    "body": raw["payload"]["issue"]["body"],
                }
            }
        elif self.type == "PullRequestEvent":
            created_at = raw["payload"]["pull_request"]["created_at"]
            if created_at:
                created_at = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%S%z')
                created_at = created_at.astimezone(timezone)

            updated_at = raw["payload"]["pull_request"]["updated_at"]
            if updated_at:
                updated_at = datetime.strptime(updated_at, '%Y-%m-%dT%H:%M:%S%z')
                updated_at = updated_at.astimezone(timezone)

            closed_at = raw["payload"]["pull_request"]["closed_at"]
            if closed_at:
                closed_at = datetime.strptime(closed_at, '%Y-%m-%dT%H:%M:%S%z')
                closed_at = closed_at.astimezone(timezone)

            merged_at = raw["payload"]["pull_request"]["merged_at"]
            if merged_at:
                merged_at = datetime.strptime(merged_at, '%Y-%m-%dT%H:%M:%S%z')
                merged_at = merged_at.astimezone(timezone)

            assignee = raw["payload"]["pull_request"]["assignee"]
            self.pull_request_data = {
                "action": raw["payload"]["action"],
                "number": raw["payload"]["number"],
                "id": raw["payload"]["pull_request"]["id"],
                "state": raw["payload"]["pull_request"]["state"],
                "title": raw["payload"]["pull_request"]["title"],
                "body": raw["payload"]["pull_request"]["body"],
                "created_at": created_at,
                "updated_at": updated_at,
                "closed_at": closed_at,
                "merged_at": merged_at,
                "merge_commit_sha": raw["payload"]["pull_request"]["merge_commit_sha"],
                "assignee": assignee.get("user", {}).get("login") if assignee else assignee,
                "assignees": [
                    user.get("login")
                    for user in raw["payload"]["pull_request"]["assignees"] if user
                ],
                "requested_reviewers": [
                    user.get("login")
                    for user in raw["payload"]["pull_request"]["requested_reviewers"] if user
                ],
                "requested_teams": [
                    user.get("login")
                    for user in raw["payload"]["pull_request"]["requested_teams"] if user
                ],
                "labels": raw["payload"]["pull_request"]["labels"],
                "draft": raw["payload"]["pull_request"]["draft"],
                "head_ref": raw["payload"]["pull_request"].get("head", {}).get("label"),
                "head_sha": raw["payload"]["pull_request"].get("head", {}).get("sha"),
                "base_ref": raw["payload"]["pull_request"].get("base", {}).get("label"),
                "base_sha": raw["payload"]["pull_request"].get("base", {}).get("sha"),
                "author_association": raw["payload"]["pull_request"]["author_association"],
                "merged": raw["payload"]["pull_request"]["merged"],
                "merged_by": raw["payload"]["pull_request"]["merged_by"],
                "comments": raw["payload"]["pull_request"]["comments"],
                "review_comments": raw["payload"]["pull_request"]["review_comments"],
                "maintainer_can_modify": raw["payload"]["pull_request"]["maintainer_can_modify"],
                "commits": raw["payload"]["pull_request"]["commits"],
                "additions": raw["payload"]["pull_request"]["additions"],
                "deletions": raw["payload"]["pull_request"]["deletions"],
                "changed_files": raw["payload"]["pull_request"]["changed_files"],
            }
        elif self.type == "PullRequestReviewCommentEvent":
            created_at = raw["payload"].get("comment", {}).get("created_at")
            if created_at:
                created_at = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%S%z')
                created_at = created_at.astimezone(timezone)

            updated_at = raw["payload"].get("comment", {}).get("updated_at")
            if updated_at:
                updated_at = datetime.strptime(updated_at, '%Y-%m-%dT%H:%M:%S%z')
                updated_at = updated_at.astimezone(timezone)

            self.pull_request_review_comment_data = {
                "action": raw["payload"]["action"],
                "comment": {
                    "user": raw["payload"].get("comment", {}).get("user", {}).get("login"),
                    "diff_hunk": raw["payload"].get("comment", {}).get("diff_hunk"),
                    "body": raw["payload"].get("comment", {}).get("body"),
                    "created_at": created_at,
                    "updated_at": updated_at,
                    "author_association": raw["payload"].get("comment", {}).get("author_association")
                },
            }

            created_at = raw["payload"]["pull_request"]["created_at"]
            if created_at:
                created_at = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%S%z')
                created_at = created_at.astimezone(timezone)

            updated_at = raw["payload"]["pull_request"]["updated_at"]
            if updated_at:
                updated_at = datetime.strptime(updated_at, '%Y-%m-%dT%H:%M:%S%z')
                updated_at = updated_at.astimezone(timezone)

            closed_at = raw["payload"]["pull_request"]["closed_at"]
            if closed_at:
                closed_at = datetime.strptime(closed_at, '%Y-%m-%dT%H:%M:%S%z')
                closed_at = closed_at.astimezone(timezone)

            merged_at = raw["payload"]["pull_request"]["merged_at"]
            if merged_at:
                merged_at = datetime.strptime(merged_at, '%Y-%m-%dT%H:%M:%S%z')
                merged_at = merged_at.astimezone(timezone)

            assignee = raw["payload"]["pull_request"]["assignee"]
            self.pull_request_review_comment_data["pull_request"] = {
                "number": raw["payload"]["pull_request"]["number"],
                "state": raw["payload"]["pull_request"]["state"],
                "title": raw["payload"]["pull_request"]["title"],
                "body": raw["payload"]["pull_request"]["body"],
                "user": raw["payload"]["pull_request"]["user"]["login"],
                "created_at": created_at,
                "updated_at": updated_at,
                "closed_at": closed_at,
                "merged_at": merged_at,
                "merge_commit_sha": raw["payload"]["pull_request"]["merge_commit_sha"],
                "assignee": assignee.get("user", {}).get("login") if assignee else assignee,
                "assignees": [
                    user.get("login")
                    for user in raw["payload"]["pull_request"]["assignees"] if user
                ],
                "requested_reviewers": [
                    user.get("login")
                    for user in raw["payload"]["pull_request"]["requested_reviewers"] if user
                ],
                "requested_teams": [
                    user.get("login")
                    for user in raw["payload"]["pull_request"]["requested_teams"] if user
                ],
                "labels": raw["payload"]["pull_request"]["labels"],
                "draft": raw["payload"]["pull_request"]["draft"],
                "head_ref": raw["payload"]["pull_request"].get("head", {}).get("label"),
                "head_sha": raw["payload"]["pull_request"].get("head", {}).get("sha"),
                "base_ref": raw["payload"]["pull_request"].get("base", {}).get("label"),
                "base_sha": raw["payload"]["pull_request"].get("base", {}).get("sha"),
                "author_association": raw["payload"]["pull_request"]["author_association"],
            }
        elif self.type == "PullRequestReviewEvent":
            submitted_at = raw["payload"].get("review", {}).get("submitted_at")
            if submitted_at:
                submitted_at = datetime.strptime(submitted_at, '%Y-%m-%dT%H:%M:%S%z')
                submitted_at = submitted_at.astimezone(timezone)

            created_at = raw["payload"]["pull_request"]["created_at"]
            if created_at:
                created_at = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%S%z')
                created_at = created_at.astimezone(timezone)

            updated_at = raw["payload"]["pull_request"]["updated_at"]
            if updated_at:
                updated_at = datetime.strptime(updated_at, '%Y-%m-%dT%H:%M:%S%z')
                updated_at = updated_at.astimezone(timezone)

            closed_at = raw["payload"]["pull_request"]["closed_at"]
            if closed_at:
                closed_at = datetime.strptime(closed_at, '%Y-%m-%dT%H:%M:%S%z')
                closed_at = closed_at.astimezone(timezone)

            merged_at = raw["payload"]["pull_request"]["merged_at"]
            if merged_at:
                merged_at = datetime.strptime(merged_at, '%Y-%m-%dT%H:%M:%S%z')
                merged_at = merged_at.astimezone(timezone)

            assignee = raw["payload"]["pull_request"]["assignee"]
            self.pull_request_review_event_data = {
                "action": raw["payload"]["action"],
                "review": {
                    "user": raw["payload"].get("review", {}).get("user", {}).get("login"),
                    "body": raw["payload"].get("review", {}).get("body"),
                    "submitted_at": submitted_at,
                    "state": raw["payload"].get("review", {}).get("state"),
                    "author_association": raw["payload"].get("review", {}).get("author_association"),
                },
                "pull_request": {
                    "number": raw["payload"]["pull_request"]["number"],
                    "state": raw["payload"]["pull_request"]["state"],
                    "title": raw["payload"]["pull_request"]["title"],
                    "body": raw["payload"]["pull_request"]["body"],
                    "user": raw["payload"]["pull_request"]["user"]["login"],
                    "created_at": created_at,
                    "updated_at": updated_at,
                    "closed_at": closed_at,
                    "merged_at": merged_at,
                    "merge_commit_sha": raw["payload"]["pull_request"]["merge_commit_sha"],
                    "assignee": assignee.get("user", {}).get("login") if assignee else assignee,
                    "assignees": [
                        user.get("login")
                        for user in raw["payload"]["pull_request"]["assignees"] if user
                    ],
                    "requested_reviewers": [
                        user.get("login")
                        for user in raw["payload"]["pull_request"]["requested_reviewers"] if user
                    ],
                    "requested_teams": [
                        user.get("login")
                        for user in raw["payload"]["pull_request"]["requested_teams"] if user
                    ],
                    "labels": raw["payload"]["pull_request"]["labels"],
                    "draft": raw["payload"]["pull_request"]["draft"],
                    "head_ref": raw["payload"]["pull_request"].get("head", {}).get("label"),
                    "head_sha": raw["payload"]["pull_request"].get("head", {}).get("sha"),
                    "base_ref": raw["payload"]["pull_request"].get("base", {}).get("label"),
                    "base_sha": raw["payload"]["pull_request"].get("base", {}).get("sha"),
                    "author_association": raw["payload"]["pull_request"]["author_association"],
                }
            }
        elif self.type == "PushEvent":
            self.push_data = {
                "ref": raw.get("payload", {}).get("ref"),
                "commits": [
                    commit["message"]
                    for commit in raw.get("payload", {}).get("commits", []) if commit
                ],
            }
        elif self.type == "WatchEvent":
            self.watch_data = {
                "action": raw.get("payload", {}).get("action"),
            }
        else:
            print("New event, you need to change the processing module and the importers")


def _fetch_details():
    details = {}
    files = get_notification_detail_file_paths()

    for file in files:
        with open(file, 'r') as json_file:
            content = json.load(json_file)
            details.update(content)
    return details


def process_notifications(input_files=None, use_details=True):
    if not input_files:
        input_files = get_notification_file_paths()

    details = None
    handled = set()
    if use_details:
        details = _fetch_details()

    for file in input_files:
        with open(file, 'r') as json_file:
            content = json.load(json_file)
            for notification in content:
                id = notification["id"]
                if id in handled:
                    continue
                else:
                    handled.add(id)
                    yield Notification(notification, details)


def process_events(input_files=None):
    if not input_files:
        input_files = get_events_file_paths()

    handled = set()
    for file in input_files:
        with open(file, 'r') as json_file:
            content = json.load(json_file)
            for event in content:
                id = event["id"]
                if id in handled:
                    continue
                else:
                    handled.add(id)
                    yield Event(raw=event)

